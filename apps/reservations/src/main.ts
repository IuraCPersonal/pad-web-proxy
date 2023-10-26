import { NestFactory } from '@nestjs/core';
import { ReservationsModule } from './reservations.module';
import { ValidationPipe } from '@nestjs/common';
import { Logger } from 'nestjs-pino';
import { ConfigService } from '@nestjs/config';
import * as cookieParser from 'cookie-parser';
import { TimeoutInterceptor } from '@app/common';
import axios from 'axios';

async function bootstrap() {
  const app = await NestFactory.create(ReservationsModule);
  const configService = app.get(ConfigService);
  const timeoutInMiliseconds: number = parseInt(
    configService.get<any>('TIMEOUT_IN_MILISECONDS', 3000),
  );

  try {
    await axios.post(configService.get('SERVICE_DISCOVERY_URL'), {
      name: configService.get('SELF_NAME'),
      host: configService.get('SELF_HOST'),
      port: configService.get('SELF_PORT'),
      type: 'reservations',
    });
  } catch (error) {
    console.error('Failed to register service:', error);
  }

  // whitelist - If set to true validator will strip validated object
  // of any properties that do not have any decorators
  app.useGlobalInterceptors(new TimeoutInterceptor(timeoutInMiliseconds));
  app.useGlobalPipes(new ValidationPipe({ whitelist: true }));
  app.useLogger(app.get(Logger));
  app.use(cookieParser());
  await app.listen(configService.get('PORT'));
}
bootstrap();
