export class Turtle {
    d: string

    constructor() {
        this.d = ""
    }

    reset() {
        this.d = ""

        return this
    }

    moveTo(x: number, y: number) {
        this.d += `M${x},${y}`

        return this
    }

    lineTo(x: number, y: number) {
        this.d += `L${x},${y}`

        return this
    }

    close() {
        this.d += `Z`

        return this
    }
}