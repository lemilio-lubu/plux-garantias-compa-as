export interface AuditAttachment {
  file_name: string;
  file_url:  string;
}

export interface Audit {
  id:                string;
  srg_id:            string;
  ot_factura:        string;
  observations:      string;
  concesionaria:     string;
  auditor_id:        string;
  additional_emails: string[];
  attachments:       AuditAttachment[];
  created_at:        string;
  updated_at:        string;
}
