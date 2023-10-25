import { CreatePaymentDto } from '@app/common';
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import Stripe from 'stripe';

@Injectable()
export class PaymentsService {
  private readonly stripe = new Stripe(
    this.configService.get('STRIPE_SECRET_KEY'),
    {
      apiVersion: '2023-10-16',
    },
  );

  constructor(private readonly configService: ConfigService) {}

  async createPayment({ amount }: CreatePaymentDto) {
    const paymentIntent = await this.stripe.paymentIntents.create({
      amount: amount * 100,
      currency: 'usd',
      payment_method: 'pm_card_visa',
    });

    return paymentIntent;
  }

  // async confirmPayment() {
  //   return await this.stripe.paymentIntents.confirm(
  //     'pm_1O2clsASgkaFpyQQdVNVDgWz',
  //     { payment_method: 'pm_card_visa' },
  //   );
  // }
}
