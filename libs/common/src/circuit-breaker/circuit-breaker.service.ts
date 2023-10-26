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

  private readonly failureThreshold = 1; // Number of failures to trigger the circuit open
  private readonly resetTimeout = 500000; // Time in milliseconds to wait before attempting to close the circuit

  async executeWithCircuitBreaker<T>(fn: () => Promise<T>): Promise<T> {
    switch (this.state) {
      case CircuitState.Closed:
        try {
          const result = await fn();
          this.consecutiveFailures = 0; // Reset failures
          return result;
        } catch (error) {
          this.consecutiveFailures++;
          if (this.consecutiveFailures >= this.failureThreshold) {
            this.state = CircuitState.Open;
            setTimeout(() => {
              this.state = CircuitState.HalfOpen;
            }, this.resetTimeout);
          }

          throw error;
        }
      case CircuitState.Open:
        throw new Error('Circuit is open');
      case CircuitState.HalfOpen:
        try {
          const result = await fn();
          this.state = CircuitState.Closed;
          this.consecutiveFailures = 0; // Reset failures
          return result;
        } catch (error) {
          this.consecutiveFailures++;
          if (this.consecutiveFailures >= this.failureThreshold) {
            this.state = CircuitState.Open;
            setTimeout(() => {
              this.state = CircuitState.HalfOpen;
            }, this.resetTimeout);
          }
          throw error;
        }
    }
  }
}
