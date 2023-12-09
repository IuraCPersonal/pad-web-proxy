import { Body, Inject, Injectable, OnModuleInit } from '@nestjs/common';
import { CreateReservationDto } from './dto/create-reservation.dto';
import { UpdateReservationDto } from './dto/update-reservation.dto';
import { ReservationsRepository } from './reservations.repository';
import { PAYMENTS_SERVICE_NAME, PaymentsServiceClient } from '@app/common';
import { ClientGrpc } from '@nestjs/microservices';
import { map } from 'rxjs';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { ReservationDocument } from './models/reservations.schema';

@Injectable()
export class ReservationsService implements OnModuleInit {
  private paymentsService: PaymentsServiceClient;

  constructor(
    private readonly reservationsRepository: ReservationsRepository,
    @Inject(PAYMENTS_SERVICE_NAME) private readonly client: ClientGrpc,
    @InjectModel('Reservations')
    private readonly reservationModel: Model<ReservationDocument>,
    @InjectModel('Payments') private readonly paymentModel: Model<any>,
  ) {}

  onModuleInit() {
    this.paymentsService = this.client.getService<PaymentsServiceClient>(
      PAYMENTS_SERVICE_NAME,
    );
  }

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

  async create_2pc(@Body() createReservationDto: CreateReservationDto) {
    const session = await this.reservationModel.db.startSession();
    session.startTransaction();
    try {
      const reservation = await this.reservationModel.create(
        [createReservationDto],
        { session },
      );
      const payment = await this.paymentModel.create(
        [{ status: 'success', reservation: reservation[0]._id }],
        { session },
      );
      if (payment[0].status !== 'success') {
        throw new Error('Payment failed');
      }
      await session.commitTransaction();
      return reservation[0];
    } catch (error) {
      await session.abortTransaction();
      throw error;
    } finally {
      session.endSession();
    }
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
}
