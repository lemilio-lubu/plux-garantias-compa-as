from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from interfaces.api.controllers.user import UserViewSet
from interfaces.api.controllers.catalog import CatalogParamViewSet, SparePartViewSet
from interfaces.api.controllers.srg import SrgViewSet
from interfaces.api.controllers.audit import AuditViewSet
from interfaces.api.controllers.dashboard import DashboardView
from interfaces.api.controllers.srg_body import (
    SrgTransitionView,
    SrgPartsView,
    SrgPartMovementView,
    SrgEventsView,
    GlobalEventsView,
    SrgCampaignBodyView,
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"catalog/params", CatalogParamViewSet, basename="catalog-params")
router.register(r"catalog/spare-parts", SparePartViewSet, basename="spare-parts")
router.register(r"srgs", SrgViewSet, basename="srgs")
router.register(r"audits", AuditViewSet, basename="audits")

urlpatterns = [
    # OpenAPI
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # Auth
    path("auth/login/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/logout/", TokenBlacklistView.as_view(), name="token-blacklist"),
    # Dashboard
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    # SRG creation by type
    path("srgs/warranty/", SrgViewSet.as_view({"post": "create_warranty"}), name="srg-warranty"),
    path("srgs/campaign/", SrgViewSet.as_view({"post": "create_campaign"}), name="srg-campaign"),
    # SRG workflow (trazabilidad)
    path("srgs/<str:srg_id>/transition/", SrgTransitionView.as_view(), name="srg-transition"),
    path("srgs/<str:srg_id>/parts/", SrgPartsView.as_view(), name="srg-parts"),
    path("srgs/<str:srg_id>/parts/<str:part_id>/movements/", SrgPartMovementView.as_view(), name="srg-part-movements"),
    path("srgs/<str:srg_id>/events/", SrgEventsView.as_view(), name="srg-events"),
    path("events/", GlobalEventsView.as_view(), name="events"),
    path("srgs/<str:srg_id>/campaign-body/", SrgCampaignBodyView.as_view(), name="srg-campaign-body"),
    # Resources
    path("", include(router.urls)),
]
