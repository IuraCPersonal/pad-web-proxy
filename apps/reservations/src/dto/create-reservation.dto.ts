import { IsDate, IsNotEmpty, IsString } from 'class-validator';
import { Type } from 'class-transformer';

export class CreateReservationDto {
  @IsDate()
  @Type(() => Date)
  startDate: Date;

  @IsDate()
  @Type(() => Date)
  endDate: Date;

  @IsString()
  @IsNotEmpty()
  userId: string;

  @IsString()
  @IsNotEmpty()
  flightId: string;

  @IsString()
  @IsNotEmpty()
  invoiceId: string;
}
