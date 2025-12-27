import apiClient from './client';

export interface CreateVisitRequest {
  phone_number: string;
  bill_id: string;
  bill_amount: number;
  verbal_consent: boolean;
  customer_name?: string;
  guest_count: number;
}

export interface VisitResponse {
  id: number;
  // Add other fields as returned by backend
}

export const visitsApi = {
  create: async (data: CreateVisitRequest): Promise<VisitResponse> => {
    const response = await apiClient.post<VisitResponse>('/visits', data);
    return response.data;
  },
};
