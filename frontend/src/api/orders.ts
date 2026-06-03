import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

export interface OrderStatusHistory {
  status: string;
  timestamp: string;
  duration_from_previous_seconds: number | null;
}

export interface Order {
  id: number;
  status: string;
  created_at: string;
  updated_at?: string;
  download_url: string | null;
  error_message: string | null;
  processing_duration_seconds: number | null;
  records_processed: number;
  status_history: OrderStatusHistory[];
}

export const getOrders = async (): Promise<Order[]> => {
  const response = await api.get("/orders/");
  return response.data;
};

export const uploadFile = async (file: File): Promise<Order> => {
  const formData = new FormData();

  formData.append("original_file", file);

  const response = await api.post("/orders/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export default api;