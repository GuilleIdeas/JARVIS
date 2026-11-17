// Tactical Consoles
export class TacticalConsoles {
  constructor(state) { this.state = state; this.interval = null; }
  start() { this.interval = setInterval(() => this.simulate(), 5000); }
  simulate() {}
}
