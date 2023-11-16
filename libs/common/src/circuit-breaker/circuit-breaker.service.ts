import { Injectable } from '@nestjs/common';

enum CircuitState {
  Closed,
  Open,
  HalfOpen,
}

@Injectable()
export class CircuitBreakerService {
  private state: CircuitState = CircuitState.Closed;
  private consecutiveFailures = 0;
  private lastAttemptTime: number = 0;

  private readonly failureThreshold = 3; // Number of failures to trigger the circuit open
  private readonly resetTimeout = 5000; // Time in milliseconds to wait before attempting to close the circuit

  async executeWithCircuitBreaker<T>(
    fn: () => Promise<T>,
    fallback: () => T,
  ): Promise<T> {
    switch (this.state) {
      case CircuitState.Closed:
        try {
          const result = await fn();
          this.consecutiveFailures = 0; // reset failure count on success
          return result;
        } catch (error) {
          this.consecutiveFailures++;
          if (this.consecutiveFailures >= this.failureThreshold) {
            this.state = CircuitState.Open;
            this.lastAttemptTime = Date.now();
            console.log('Circuit opened');
          }
          throw error;
        }
      case CircuitState.Open:
        if (Date.now() > this.lastAttemptTime + this.resetTimeout) {
          this.state = CircuitState.HalfOpen;
          console.log('Circuit half-open');
        } else {
          console.log('Circuit open, executing fallback function');
          return fallback();
        }
      // intentional fallthrough
      case CircuitState.HalfOpen:
        try {
          const result = await fn();
          this.state = CircuitState.Closed;
          this.consecutiveFailures = 0; // reset failure count on success
          console.log('Circuit closed');
          return result;
        } catch (error) {
          this.state = CircuitState.Open;
          this.lastAttemptTime = Date.now();
          console.log('Circuit opened');
          throw error;
        }
    }
  }
}
