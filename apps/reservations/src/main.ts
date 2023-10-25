import { NestFactory } from '@nestjs/core';
import { ReservationsModule } from './reservations.module';
import { ValidationPipe } from '@nestjs/common';
import { Logger } from 'nestjs-pino';
import { ConfigService } from '@nestjs/config';
import * as cookieParser from 'cookie-parser';
import { TimeoutInterceptor } from '@app/common';

async function bootstrap() {
  const app = await NestFactory.create(ReservationsModule);
  const configService = app.get(ConfigService);
  const timeoutInMiliseconds: number = parseInt(
    configService.get<any>('TIMEOUT_IN_MILISECONDS', 3000),
  );

  // whitelist - If set to true validator will strip validated object
  // of any properties that do not have any decorators
  app.useGlobalInterceptors(new TimeoutInterceptor(timeoutInMiliseconds));
  app.useGlobalPipes(new ValidationPipe({ whitelist: true }));
  app.useLogger(app.get(Logger));
  app.use(cookieParser());
  await app.listen(configService.get('PORT'));
}
bootstrap();
