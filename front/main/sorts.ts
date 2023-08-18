/*
 * Animated sorts
 * Copyright (C) 2023 Jonathan Tremesaygues
 *
 * sorts.ts
 *
 * This program is free software: you can redistribute it and/or modify it under
 * the terms of the GNU General Public License as published by the Free Software
 * Foundation, either version 3 of the License, or (at your option) any later
 * version.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with
 * this program. If not, see <https://www.gnu.org/licenses/>.
 */

function lerp(x: number, x0: number, x1: number, y0: number, y1: number): number {
    return y0 + (x - x0) * (y1 - y0) / (x1 - x0)
}

// randint() in [a, b[
function randint(a: number = 0, b: number = 2 * 32): number {
    return Math.floor(lerp(Math.random(), 0, 1, a, b))
}

function swap(array: Array<number>, a: number, b: number): Array<number> {
    let tmp = array[a]
    array[a] = array[b]
    array[b] = tmp

    return array
}

function shuffle(array: Array<number>): Array<number> {
    for (let i = 0; i < array.length - 1; ++i) {
        swap(array, i, randint(i, array.length))
    }

    return array
}

function* bubble_sort(samples: Array<number>): Generator {
    let swapped = false
    do {
        swapped = false
        for (let i = 1; i < samples.length; ++i) {
            if (samples[i - 1] > samples[i]) {
                swap(samples, i, i - 1)
                swapped = true
                yield
            }
        }
    } while (swapped)
}

function* insertion_sort(samples: Array<number>): Generator {
    for (let i = 1; i < samples.length; ++i) {
        let j = i
        while (j > 0 && samples[j - 1] > samples[j]) {
            swap(samples, j, j - 1)
            j--
            yield
        }
    }
}

function* odd_even_sort(samples: Array<number>): Generator {
    let sorted = false
    while (!sorted) {
        for (let j = 0; j < 2; ++j) {
            sorted = true
            for (let i = 1; i < samples.length - 1; i += 2) {
                if (samples[i] > samples[i + 1]) {
                    swap(samples, i, i + 1);
                    sorted = false;
                    yield
                }
            }
        }
        sorted = true
        for (let i = 0; i < samples.length - 1; i += 2) {
            if (samples[i] > samples[i + 1]) {
                swap(samples, i, i + 1);
                sorted = false;
                yield
            }
        }
    }
}


class Engine {
    canvas: HTMLCanvasElement
    sorter_selector: HTMLSelectElement
    samples_count: HTMLInputElement
    playback: HTMLInputElement
    ctx: CanvasRenderingContext2D
    samples: Array<number>
    sorter: Generator | null
    sorters: Map<string, (samples: Array<number>) => Generator> = new Map([
        ["bubble", bubble_sort],
        ["insertion", insertion_sort],
        ["odd_even", odd_even_sort]
    ])

    constructor(app_id: string = "app") {
        let app = document.getElementById(app_id)!
        this.canvas = app.querySelector("[name=canvas]") as HTMLCanvasElement
        this.ctx = this.canvas.getContext("2d")!
        this.sorter_selector = app.querySelector("[name=sort]")!
        this.sorter_selector.addEventListener("change", this.start.bind(this))
        this.samples_count = app.querySelector("[name=samples_count]")!
        this.samples_count.addEventListener("change", this.start.bind(this))
        this.playback = app.querySelector("[name=playback]")!
        app.querySelector("[name=reset]")?.addEventListener("click", this.start.bind(this))

        this.samples = []
        this.sorter = null
        this.sorters.forEach((_fn, name) => {
            let node = document.createElement("option")
            node.label = name
            node.value = name
            this.sorter_selector.appendChild(node)
        })
    }

    update(_time: DOMHighResTimeStamp) {
        if (this.playback.checked && this.sorter != null) {
            this.sorter.next()
        }

        // Clear
        this.ctx.fillStyle = "#333"
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height)

        this.ctx.save()
        // Flip Y, so 0 is bottom and Y-max is up
        this.ctx.scale(1, -1)
        this.ctx.translate(0, -this.canvas.height)

        // Fill the entire canvas with the bars
        this.ctx.scale(this.canvas.width / this.samples.length, this.canvas.height / this.samples.length)

        // Draw the bar
        this.samples.forEach((sample, i) => {
            this.ctx.fillStyle = `hsl(${lerp(sample, 0, this.samples.length, 0, 360)}, 100%, 50%)`
            this.ctx.fillRect(i, 0, 1, sample)
        })
        this.ctx.restore()
        this.schedule_update()
    }

    schedule_update() {
        window.requestAnimationFrame(this.update.bind(this))
    }

    start() {
        let fn = this.sorters.get(this.sorter_selector.value)
        if (fn != null) {
            this.samples = shuffle(Array(Math.pow(2, parseInt(this.samples_count.value))).fill(0).map((_k, i) => i))
            this.sorter = fn(this.samples)
        }
        this.schedule_update()
    }
}

new Engine().start()