import { Controller, Get } from '@nestjs/common';
import { PaymentsService } from './payments.service';
import { MessagePattern, Payload } from '@nestjs/microservices';
import { CreatePaymentDto } from '../dto/create-payment.dto';

@Controller()
export class PaymentsController {
  constructor(private readonly paymentsService: PaymentsService) {}

  @MessagePattern('create_payment')
  async createPayment(@Payload() data: CreatePaymentDto) {
    return this.paymentsService.createPayment(data);
  }
}
