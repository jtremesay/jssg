let app = document.getElementById("app")!
let canvas = app.querySelector("canvas[name=canvas]")! as HTMLCanvasElement
let samples_count_input = app.querySelector("input[name=samples_count]")! as HTMLInputElement
let samples_in_cirle_input = app.querySelector("input[name=samples_in_circle]")! as HTMLInputElement
let ratio_input = app.querySelector("input[name=ratio]")! as HTMLInputElement
let ctx = canvas.getContext("2d")!

// Clear
ctx.fillStyle = "#333"
ctx.fillRect(0, 0, canvas.width, canvas.height)

let samples_count = 0
let samples_in_circle = 0

function update() {
    for (let i = 0; i < 1000; ++i) {
        let x = Math.random()
        let y = Math.random()

        samples_count++
        if (Math.sqrt(Math.pow(x - 0.5, 2) + Math.pow(y - 0.5, 2)) <= 0.5) {
            ctx.fillStyle = "#0d0"
            samples_in_circle++
        } else {

            ctx.fillStyle = "#d00"
        }

        ctx.fillRect(x * canvas.width, y * canvas.height, 1, 1)
    }
    samples_count_input.value = samples_count.toString()
    samples_in_cirle_input.value = samples_in_circle.toString()
    ratio_input.value = (4 * samples_in_circle / samples_count).toString()

    window.requestAnimationFrame(update)
}

window.requestAnimationFrame(update)
