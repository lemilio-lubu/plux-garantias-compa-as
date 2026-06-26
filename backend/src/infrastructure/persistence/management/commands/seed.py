"""Seed the database with demo data for local development and showcasing the UI.

Creates one login account per role plus a realistic set of SRGs (warranty and
campaign), catalog parameters, spare parts and audits spread across the three
dealerships. The command is idempotent: running it again updates the existing
rows instead of duplicating them.

Usage:
    python manage.py seed
    python manage.py seed --flush   # wipe demo SRGs/audits first, then reseed
"""

from __future__ import annotations

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from infrastructure.persistence.models.audit import Audit
from infrastructure.persistence.models.catalog import (
    CatalogParam,
    CatalogParamType,
    SparePart,
)
from infrastructure.persistence.models.srg import Srg, SrgStatus, SrgType
from infrastructure.persistence.models.srg_body import (
    CampaignBody,
    SrgEvent,
    SrgEventType,
    SrgPart,
)
from infrastructure.persistence.models.user import Concesionaria, User, UserRole

DEMO_PASSWORD = "Plux2024!"

# ── Login accounts (documented in the README) ──────────────────────────────
# One account per role. The advisor accounts for the other dealerships exist
# only so cross-dealership SRGs have a valid owner; they share DEMO_PASSWORD.
ACCOUNTS = [
    ("superadmin@plux.com", "Sara",   "Núñez",    UserRole.SUPER_ADMIN, ""),
    ("jefe@plux.com",       "Hernán", "Vélez",    UserRole.JEFE_TALLER, Concesionaria.SURMOTOR),
    ("asesor@plux.com",     "Daniela","Yépez",    UserRole.ASESOR,      Concesionaria.SURMOTOR),
    ("bodeguero@plux.com",  "Marco",  "Tapia",    UserRole.BODEGUERO,   Concesionaria.SURMOTOR),
    ("auditor@plux.com",    "Lucía",  "Andrade",  UserRole.AUDITOR,     Concesionaria.SURMOTOR),
    # Extra advisors so the consolidated (super-admin) view spans dealerships.
    ("asesor.granda@plux.com", "Pablo",  "Mejía",  UserRole.ASESOR, Concesionaria.GRANDA_CENTENO),
    ("asesor.shyris@plux.com", "Camila", "Vaca",   UserRole.ASESOR, Concesionaria.SHYRIS),
]

# ── Catalog seed data, keyed by dealership ─────────────────────────────────
VEHICLE_MODELS = {
    Concesionaria.SURMOTOR: [
        ("SAIL", "Chevrolet Sail"),
        ("DMAX", "Chevrolet D-Max"),
        ("ONIX", "Chevrolet Onix"),
    ],
    Concesionaria.GRANDA_CENTENO: [
        ("VITARA", "Suzuki Vitara"),
        ("SWIFT", "Suzuki Swift"),
        ("ERTIGA", "Suzuki Ertiga"),
    ],
    Concesionaria.SHYRIS: [
        ("SPORTAGE", "Kia Sportage"),
        ("RIO", "Kia Rio"),
        ("SELTOS", "Kia Seltos"),
    ],
}

COLORS = [("BLK", "Negro Ónix"), ("WHT", "Blanco Glaciar"), ("SLV", "Plata Metálico"), ("RED", "Rojo Lava")]

WARRANTY_TYPES = [
    ("WT01", "Defecto de fabricación - motor"),
    ("WT02", "Falla eléctrica - tablero"),
    ("WT03", "Desgaste prematuro - frenos"),
    ("WT04", "Fuga - sistema de refrigeración"),
]

CAMPAIGN_CODES = [
    ("CM-2024-07", "Recall airbag conductor"),
    ("CM-2024-11", "Actualización software ECU"),
]

SPARE_PARTS = {
    Concesionaria.SURMOTOR: [
        ("SP-1001", "Bomba de agua", "84.50"),
        ("SP-1002", "Pastillas de freno (juego)", "62.00"),
        ("SP-1003", "Sensor de oxígeno", "121.75"),
    ],
    Concesionaria.GRANDA_CENTENO: [
        ("SP-2001", "Módulo airbag", "310.00"),
        ("SP-2002", "Radiador", "198.40"),
    ],
    Concesionaria.SHYRIS: [
        ("SP-3001", "Unidad de control ECU", "540.00"),
        ("SP-3002", "Alternador", "265.90"),
    ],
}


def _vin(seq: int) -> str:
    """Deterministic 17-char VIN-like identifier."""
    base = f"8LDKB48E{seq:09d}"
    return base[:17].upper()


class Command(BaseCommand):
    help = "Seed the database with demo users and SRG data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing demo SRGs and audits before seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["flush"]:
            Audit.objects.all().delete()
            SrgEvent.objects.all().delete()
            SrgPart.objects.all().delete()
            CampaignBody.objects.all().delete()
            Srg.objects.all().delete()
            self.stdout.write(self.style.WARNING("Flushed existing SRGs and audits."))

        users = self._seed_users()
        self._seed_catalog()
        srgs = self._seed_srgs(users)
        self._seed_audits(srgs, users["auditor@plux.com"])

        self.stdout.write(self.style.SUCCESS("\nSeed complete."))
        self.stdout.write(f"  Users:   {User.objects.count()}")
        self.stdout.write(f"  SRGs:    {Srg.objects.count()}")
        self.stdout.write(f"  Catalog: {CatalogParam.objects.count()} params, {SparePart.objects.count()} parts")
        self.stdout.write(f"  Parts:   {SrgPart.objects.count()} on SRGs, {SrgEvent.objects.count()} trace events")
        self.stdout.write(f"  Audits:  {Audit.objects.count()}")
        self.stdout.write(self.style.HTTP_INFO(f"\n  All demo accounts use the password: {DEMO_PASSWORD}"))

    # ── Users ──────────────────────────────────────────────────────────────
    def _seed_users(self) -> dict[str, User]:
        users: dict[str, User] = {}
        for email, first, last, role, dealer in ACCOUNTS:
            user, _ = User.objects.get_or_create(email=email)
            user.first_name = first
            user.last_name = last
            user.role = role
            user.concesionaria = dealer
            user.is_active = True
            user.is_staff = role == UserRole.SUPER_ADMIN
            user.is_superuser = role == UserRole.SUPER_ADMIN
            user.set_password(DEMO_PASSWORD)
            user.save()
            users[email] = user
        self.stdout.write(self.style.SUCCESS(f"Users ready ({len(users)})."))
        return users

    # ── Catalog ────────────────────────────────────────────────────────────
    def _seed_catalog(self) -> None:
        for dealer in Concesionaria.values:
            for code, name in VEHICLE_MODELS[dealer]:
                self._param(CatalogParamType.VEHICLE_MODEL, code, name, dealer)
            for code, name in COLORS:
                self._param(CatalogParamType.COLOR, code, name, dealer)
            for code, name in WARRANTY_TYPES:
                self._param(CatalogParamType.WARRANTY_TYPE, code, name, dealer)
            for code, name in CAMPAIGN_CODES:
                self._param(CatalogParamType.CAMPAIGN_CODE, code, name, dealer)
            for code, name, price in SPARE_PARTS[dealer]:
                SparePart.objects.update_or_create(
                    catalog_code=code,
                    concesionaria=dealer,
                    defaults={"name": name, "unit_price": price},
                )
        self.stdout.write(self.style.SUCCESS("Catalog ready."))

    def _param(self, param_type, code, name, dealer) -> None:
        CatalogParam.objects.update_or_create(
            param_type=param_type,
            code=code,
            concesionaria=dealer,
            defaults={"name": name},
        )

    # ── SRGs ───────────────────────────────────────────────────────────────
    def _seed_srgs(self, users: dict[str, User]) -> list[Srg]:
        advisor = {
            Concesionaria.SURMOTOR: users["asesor@plux.com"],
            Concesionaria.GRANDA_CENTENO: users["asesor.granda@plux.com"],
            Concesionaria.SHYRIS: users["asesor.shyris@plux.com"],
        }
        now = timezone.now()

        # (ot_seq, type, status, dealer, model_idx, warranty_idx_or_campaign_idx)
        plan = [
            (1,  SrgType.WARRANTY, SrgStatus.PROCESO,     Concesionaria.SURMOTOR,        0, 0),
            (2,  SrgType.WARRANTY, SrgStatus.PENDIENTE,   Concesionaria.SURMOTOR,        1, 1),
            (3,  SrgType.WARRANTY, SrgStatus.PREAPROBADO, Concesionaria.SURMOTOR,        2, 2),
            (4,  SrgType.WARRANTY, SrgStatus.APROBADO,    Concesionaria.SURMOTOR,        0, 3),
            (5,  SrgType.WARRANTY, SrgStatus.APROBADO,    Concesionaria.SURMOTOR,        1, 0),
            (6,  SrgType.WARRANTY, SrgStatus.NEGADO,      Concesionaria.SURMOTOR,        2, 1),
            (7,  SrgType.WARRANTY, SrgStatus.RETORNADO,   Concesionaria.SURMOTOR,        0, 2),
            (8,  SrgType.CAMPAIGN, SrgStatus.PROCESO,     Concesionaria.SURMOTOR,        1, 0),
            (9,  SrgType.CAMPAIGN, SrgStatus.APROBADO,    Concesionaria.SURMOTOR,        2, 1),
            (10, SrgType.WARRANTY, SrgStatus.PENDIENTE,   Concesionaria.GRANDA_CENTENO,  0, 0),
            (11, SrgType.WARRANTY, SrgStatus.APROBADO,    Concesionaria.GRANDA_CENTENO,  1, 1),
            (12, SrgType.CAMPAIGN, SrgStatus.APROBADO,    Concesionaria.GRANDA_CENTENO,  2, 0),
            (13, SrgType.WARRANTY, SrgStatus.PREAPROBADO, Concesionaria.SHYRIS,          0, 2),
            (14, SrgType.WARRANTY, SrgStatus.APROBADO,    Concesionaria.SHYRIS,          1, 3),
            (15, SrgType.CAMPAIGN, SrgStatus.PROCESO,     Concesionaria.SHYRIS,          2, 1),
        ]

        srgs: list[Srg] = []
        for seq, srg_type, status, dealer, model_idx, idx in plan:
            _, model_name = VEHICLE_MODELS[dealer][model_idx]
            _, color_name = COLORS[seq % len(COLORS)]
            km_open = 12000 + seq * 1850
            approved = status == SrgStatus.APROBADO

            defaults = {
                "srg_type": srg_type,
                "status": status,
                "concesionaria": dealer,
                "asesor": advisor[dealer],
                "vin": _vin(seq),
                "vehicle_model": model_name,
                "vehicle_color": color_name,
                "vehicle_year": 2019 + (seq % 6),
                "km_apertura": km_open,
                "sede": dealer,
                "fecha_envio_marca": now - timedelta(days=seq) if status != SrgStatus.PROCESO else None,
                "fecha_aprobacion": (now - timedelta(days=seq - 1)).date() if approved else None,
            }

            if srg_type == SrgType.WARRANTY:
                wt_code, wt_name = WARRANTY_TYPES[idx]
                defaults.update(
                    {
                        "nro_garantia": f"GAR-{2024}{seq:04d}",
                        "warranty_type_code": wt_code,
                        "warranty_type_name": wt_name,
                    }
                )
            else:
                camp_code, _ = CAMPAIGN_CODES[idx % len(CAMPAIGN_CODES)]
                defaults["campaign_code"] = camp_code

            srg, _ = Srg.objects.update_or_create(ot=f"OT-2024-{seq:04d}", defaults=defaults)
            srgs.append(srg)

            # Parts/checklist are available once a warranty is sent to the brand
            # (PENDIENTE onward). Demo data only seeds them on APROBADO SRGs so the
            # sample checklists are fully populated.
            if srg_type == SrgType.WARRANTY and status == SrgStatus.APROBADO:
                self._seed_parts_and_checklist(srg, dealer, advisor[dealer], users["bodeguero@plux.com"])
            if srg_type == SrgType.CAMPAIGN:
                CampaignBody.objects.update_or_create(
                    srg=srg,
                    defaults={
                        "update_name": CAMPAIGN_CODES[idx % len(CAMPAIGN_CODES)][1],
                        "image_link": "https://placehold.co/600x400?text=Campaign",
                        "modified_by": advisor[dealer].full_name,
                    },
                )

        self.stdout.write(self.style.SUCCESS(f"SRGs ready ({len(srgs)})."))
        return srgs

    def _seed_parts_and_checklist(
        self, srg: Srg, dealer: Concesionaria, advisor: User, bodeguero: User
    ) -> None:
        """Seed parts with a realistic trace of reception / work / return events.

        Part 1 runs the full flow (received complete, installed, cores returned
        and confirmed). Part 2 shows a partial reception (3 of 5) still pending.
        """
        catalog = SPARE_PARTS[dealer][:2]
        plans = [
            {"qty": 2, "received": 2, "used": 2, "ret_decl": 2, "ret_conf": 2},
            {"qty": 5, "received": 3, "used": 0, "ret_decl": 0, "ret_conf": 0},
        ]
        for (code, name, price), plan in zip(catalog, plans):
            part, _ = SrgPart.objects.get_or_create(
                srg=srg,
                catalog_code=code,
                defaults={
                    "name_es": name.upper(),
                    "quantity": plan["qty"],
                    "unit_price": price,
                    "part_origin": "ORIGINAL",
                    "invoice_number": f"FAC-{srg.ot[-4:]}",
                },
            )
            SrgEvent.objects.filter(srg_part=part).delete()
            self._event(srg, part, advisor, UserRole.ASESOR, SrgEventType.PART_REQUESTED, plan["qty"])
            if plan["received"]:
                self._event(srg, part, bodeguero, UserRole.BODEGUERO, SrgEventType.RECEPTION_REGISTERED, plan["received"])
            if plan["used"]:
                self._event(srg, part, advisor, UserRole.ASESOR, SrgEventType.WORK_REGISTERED, plan["used"])
            if plan["ret_decl"]:
                self._event(srg, part, advisor, UserRole.ASESOR, SrgEventType.CORE_RETURN_DECLARED, plan["ret_decl"])
            if plan["ret_conf"]:
                self._event(srg, part, bodeguero, UserRole.BODEGUERO, SrgEventType.RETURN_CONFIRMED, plan["ret_conf"])

    def _event(self, srg, part, actor, role, event_type, qty) -> None:
        SrgEvent.objects.create(
            srg=srg, srg_part=part, actor=actor, actor_role=role,
            event_type=event_type, quantity=qty,
        )

    # ── Audits ─────────────────────────────────────────────────────────────
    def _seed_audits(self, srgs: list[Srg], auditor: User) -> None:
        approved_surmotor = [
            s
            for s in srgs
            if s.status == SrgStatus.APROBADO and s.concesionaria == Concesionaria.SURMOTOR
        ]
        for srg in approved_surmotor:
            Audit.objects.update_or_create(
                srg=srg,
                defaults={
                    "ot_factura": f"FAC-{srg.ot[-4:]}",
                    "observations": "Documentación revisada y conforme. Repuesto causal verificado contra factura.",
                    "concesionaria": srg.concesionaria,
                    "auditor": auditor,
                    "additional_emails": ["garantias@plux.com"],
                    "attachments": [],
                },
            )
        self.stdout.write(self.style.SUCCESS(f"Audits ready ({len(approved_surmotor)})."))
