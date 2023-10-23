import { Controller, Post } from '@nestjs/common';
import { PaymentsService } from './payments.service';
import { MessagePattern, Payload } from '@nestjs/microservices';
import { CreatePaymentDto } from '@app/common';

@Controller()
export class PaymentsController {
  constructor(private readonly paymentsService: PaymentsService) {}

  @MessagePattern('create_payment')
  async createPayment(@Payload() data: CreatePaymentDto) {
    return this.paymentsService.createPayment(data);
  }

  @Post('/confirm')
  async confirmPayment() {
    return this.paymentsService.confirmPayment();
  }
}
