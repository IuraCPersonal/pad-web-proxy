import { Controller, UsePipes, ValidationPipe } from '@nestjs/common';
import { PaymentsService } from './payments.service';
import {
  CreatePaymentDto,
  PaymentsServiceController,
  PaymentsServiceControllerMethods,
} from '@app/common';

@Controller()
@PaymentsServiceControllerMethods()
export class PaymentsController implements PaymentsServiceController {
  constructor(private readonly paymentsService: PaymentsService) {}

  @UsePipes(new ValidationPipe())
  async createPayment(data: CreatePaymentDto) {
    return this.paymentsService.createPayment(data);
  }

  // @Post('/confirm')
  // async confirmPayment() {
  //   return this.paymentsService.confirmPayment();
  // }
}
