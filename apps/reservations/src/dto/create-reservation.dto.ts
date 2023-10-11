export class CreateReservationDto {
  startDate: Date;
  endDate: Date;
  userId: string;
  flightId: string;
  invoiceId: string;
}
