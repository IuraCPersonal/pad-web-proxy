import { Inject, Injectable, OnModuleInit } from '@nestjs/common';
import { CreateReservationDto } from './dto/create-reservation.dto';
import { UpdateReservationDto } from './dto/update-reservation.dto';
import { ReservationsRepository } from './reservations.repository';
import { PAYMENTS_SERVICE_NAME, PaymentsServiceClient } from '@app/common';
import { ClientGrpc } from '@nestjs/microservices';
import { map } from 'rxjs';

@Injectable()
export class ReservationsService implements OnModuleInit {
  private paymentsService: PaymentsServiceClient;

  constructor(
    private readonly reservationsRepository: ReservationsRepository,
    @Inject(PAYMENTS_SERVICE_NAME) private readonly client: ClientGrpc,
  ) {}

  onModuleInit() {
    this.paymentsService = this.client.getService<PaymentsServiceClient>(
      PAYMENTS_SERVICE_NAME,
    );
  }

  //   async create(createReservationDto: CreateReservationDto, userId: string) {
  //   // Phase 1: Prepare
  //   // Start a transaction in the reservations service
  //   const reservationTransaction = await this.reservationsRepository.startTransaction();

  //   // Prepare the reservation
  //   const reservation = this.reservationsRepository.create({
  //     ...createReservationDto,
  //     timestamp: new Date(),
  //     userId,
  //   });

  //   // Save the reservation in the database, but don't commit the transaction yet
  //   await this.reservationsRepository.save(reservation, { session: reservationTransaction });

  //   // Prepare the payment
  //   const payment = await this.paymentsService.createPayment(createReservationDto.payment);

  //   // Phase 2: Commit or Rollback
  //   if (payment.status === 'success') {
  //     // If the payment was successful, commit the reservation transaction
  //     await reservationTransaction.commit();
  //     reservation.invoiceId = payment.id;
  //     return reservation;
  //   } else {
  //     // If the payment failed, rollback the reservation transaction
  //     await reservationTransaction.rollback();
  //     throw new Error('Payment failed');
  //   }
  // }

  async create(createReservationDto: CreateReservationDto, userId: string) {
    return this.paymentsService
      .createPayment(createReservationDto.payment)
      .pipe(
        map((res) => {
          return this.reservationsRepository.create({
            ...createReservationDto,
            invoiceId: res.id,
            timestamp: new Date(),
            userId,
          });
        }),
      );
  }

  async findAll() {
    return this.reservationsRepository.find({});
  }

  async findOne(_id: string) {
    return this.reservationsRepository.findOne({ _id });
  }

  async update(_id: string, updateReservationDto: UpdateReservationDto) {
    return this.reservationsRepository.findOneAndUpdate(
      { _id },
      { $set: updateReservationDto },
    );
  }

  async remove(_id: string) {
    return this.reservationsRepository.findOneAndDelete({ _id });
  }

  async simulate_failure() {
    throw new Error('Simulated server error');
  }
}
