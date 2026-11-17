// System Metrics
export class SystemMetrics {
  constructor(state) { this.state = state; this.interval = null; }
  start() { this.interval = setInterval(() => this.update(), 2000); }
  update() {}
}
