import { ChargingPile } from './charging-pile.model';

export interface ChargingRecord {
  id: number;
  record_no: string;
  pile_id: number;
  pile_detail?: ChargingPile;
  vehicle_id?: number;
  plate_number: string;
  kwh: string;
  duration_minutes: number;
  total_fee: string;
  start_time: string;
  end_time: string;
  created_at: string;
}
