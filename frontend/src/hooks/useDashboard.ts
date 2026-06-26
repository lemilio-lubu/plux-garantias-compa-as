import { useQuery } from "@tanstack/react-query";
import { dashboardService } from "@/services/dashboard.service";

export function useDashboard(concesionaria?: string) {
  return useQuery({
    queryKey: ["dashboard", concesionaria],
    queryFn:  () => dashboardService.get(concesionaria),
    refetchInterval: 1000 * 60, // refresca cada minuto
  });
}
