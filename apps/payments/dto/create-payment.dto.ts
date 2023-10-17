import Stripe from 'stripe';

export class CreatePaymentDto {
  card: Stripe.PaymentMethodCreateParams.Card1;
  amount: number;
}
