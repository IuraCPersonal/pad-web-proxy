/* eslint-disable */
import { GrpcMethod, GrpcStreamMethod } from "@nestjs/microservices";
import { Observable } from "rxjs";

export const protobufPackage = "payments";

export interface CreatePaymentMessage {
  amount: number;
  card: CardMessage | undefined;
}

export interface CardMessage {
  cvc: string;
  expMonth: number;
  expYear: number;
  number: string;
}

export interface CreatePaymentsResponse {
  id: string;
}

export const PAYMENTS_PACKAGE_NAME = "payments";

export interface PaymentsServiceClient {
  createPayment(request: CreatePaymentMessage): Observable<CreatePaymentsResponse>;
}

export interface PaymentsServiceController {
  createPayment(
    request: CreatePaymentMessage,
  ): Promise<CreatePaymentsResponse> | Observable<CreatePaymentsResponse> | CreatePaymentsResponse;
}

export function PaymentsServiceControllerMethods() {
  return function (constructor: Function) {
    const grpcMethods: string[] = ["createPayment"];
    for (const method of grpcMethods) {
      const descriptor: any = Reflect.getOwnPropertyDescriptor(constructor.prototype, method);
      GrpcMethod("PaymentsService", method)(constructor.prototype[method], method, descriptor);
    }
    const grpcStreamMethods: string[] = [];
    for (const method of grpcStreamMethods) {
      const descriptor: any = Reflect.getOwnPropertyDescriptor(constructor.prototype, method);
      GrpcStreamMethod("PaymentsService", method)(constructor.prototype[method], method, descriptor);
    }
  };
}

export const PAYMENTS_SERVICE_NAME = "PaymentsService";
