import axios from 'axios';

const API_URL = 'http://localhost:8000/api'; // V0: Hardcoded local backend

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types
export interface AuditLog {
  id: string; // UUID
  timestamp: string;
  actor_type: 'STAFF' | 'CUSTOMER' | 'OWNER' | 'PLATFORM_ADMIN' | 'SYSTEM';
  actor_id?: number;
  event_name: string;
  target_resource: string;
  payload: Record<string, unknown>;
}

export interface VisitStats {
  visits_today: number;
  checkins_today: number;
  redemptions_today: number;
}

// Admin Service
export const adminService = {
  getAuditLogs: async (): Promise<AuditLog[]> => {
    // Defines a new endpoint we need to create in Backend: GET /admin/audits
    const response = await api.get<AuditLog[]>('/admin/audits');
    return response.data;
  },
  
  getDashboardStats: async (): Promise<VisitStats> => {
     // Defines a new endpoint: GET /admin/stats
     const response = await api.get<VisitStats>('/admin/stats');
     return response.data;
  }
};
