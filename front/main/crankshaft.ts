import * as d3 from "d3"

const PIN_RADIUS = 10
const PISTON_HEIGHT = PIN_RADIUS + 40
const PISTON_RADIUS = 50

class Engine {
    should_run: boolean

    crankshaft_radius: number
    rod_length: number

    text_infos_node: d3.BaseType
    piston_node: d3.BaseType
    rod_node: d3.BaseType
    crankshaft_pin_node: d3.BaseType
    piston_pin_node: d3.BaseType

    constructor(crankshaft_radius: number, rod_length: number, container: d3.BaseType) {
        this.should_run = true

        this.crankshaft_radius = crankshaft_radius
        this.rod_length = rod_length

        let width = 400
        let height = 800

        let $svg = d3.select(container)
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [0, 0, width, height])
            .attr("style", "background-color: grey")

        // Bodies
        let $bodies = $svg.append("g")
            .attr("transform", `translate(${width / 2}, ${height - 150})`)

        // Crankshaft
        $bodies.append("circle")
            .attr("r", this.crankshaft_radius)
            .attr("style", "fill: red")

        // Piston
        this.piston_node = $bodies.append("line")
            .attr("y2", -PISTON_HEIGHT)
            .attr("style", `stroke: blue; stroke-width: ${PISTON_RADIUS * 2}`)
            .node()

        // Rod
        this.rod_node = $bodies.append("line")
            .attr("y2", -this.rod_length)
            .attr("style", `stroke: green; stroke-width: ${PIN_RADIUS * 2}`)
            .node()

        // Crank pin
        this.crankshaft_pin_node = $bodies.append("circle")
            .attr("r", PIN_RADIUS)
            .attr("style", "fill: pink")
            .node()

        // Piston pin
        this.piston_pin_node = $bodies.append("circle")
            .attr("r", PIN_RADIUS)
            .attr("style", "fill: pink")
            .node()

        // Text infos
        this.text_infos_node = $svg.append("g")
            .attr("transform", "translate(5, 20)").node()

    }

    update(dt: DOMHighResTimeStamp) {
        let theta = dt / 1000

        let tdc_y = this.crankshaft_radius + this.rod_length
        //let bdc_y = -this.crankshaft_radius + this.rod_length

        let piston_y = -(this.crankshaft_radius * Math.cos(theta) + Math.sqrt(Math.pow(this.rod_length, 2) - Math.pow(this.crankshaft_radius, 2) * Math.pow(Math.sin(theta), 2)))

        let piston_yrel = tdc_y - piston_y
        //let cylinder_ratio = 0
        // Infos
        d3.select(this.text_infos_node).selectAll("text")
            .data([
                `Crankshaft radius: ${this.crankshaft_radius} units`,
                `Crankshaft theta: ${(theta % (2 * Math.PI)).toFixed(1)} rad`,
                `Crankshaft ang. vel.: 60 RPM`,
                `Crankshaft lin. vel.: ${(2 * this.crankshaft_radius * Math.PI).toFixed(1)} units.s⁻¹`,
                `Rod length: ${this.rod_length} units`,
                `Rod / Crankshaft ratio: ${(this.rod_length / this.crankshaft_radius).toFixed(2)}`,
                `Rod theta: TODO rad`,
                `Piston radius: ${PISTON_RADIUS} units`,
                `Piston height: ${PISTON_HEIGHT} units`,
                `Piston y: ${piston_yrel.toFixed(0)} units`,
                `Cylinder volume: ${((PISTON_RADIUS * PISTON_RADIUS * Math.PI) * (this.crankshaft_radius * 2) / 1000).toFixed(1)} kunits³`,
                `Cylinder current volume: TODO units³`,
                `Cylinder compression ratio: TODO`,])
            .join("text")
            .attr("y", (_d, i) => i * 20)
            .text((d) => d)

        // Piston
        d3.select(this.piston_node)
            .attr("transform", [
                `translate(0, ${piston_y})`,
            ])

        // Rod
        d3.select(this.rod_node)
            .attr("transform", [
                `translate(0, ${piston_y})`,
                `rotate(${(-Math.asin(Math.sin(theta) * this.crankshaft_radius / this.rod_length)) * 180 / Math.PI})`
            ])

        // Crankshaft pin
        d3.select(this.crankshaft_pin_node)
            .attr("transform", [
                `translate(0, ${-this.crankshaft_radius})`,
                `rotate(${theta * 180 / Math.PI}, 0, ${this.crankshaft_radius})`])

        // Piston pin
        d3.select(this.piston_pin_node)
            .attr("transform", [`translate(0, ${piston_y})`])
    }

    run() {
        this.should_run = true
        window.requestAnimationFrame((dt: DOMHighResTimeStamp) => {
            this.update(dt)
            if (this.should_run) {
                this.run()
            }
        })
    }
}



d3.select("#app").call(function ($app) {

    let crankshaft_radiuses = [20, 50, 100]
    let rod_scales = [2, 2.5, 3, 3.5, 4]

    $app.append("table").call(($table) => {
        $table.append("thead").call(($thead) => {
            $thead.append("tr").call(($tr) => {
                $tr.append("th").text("Rod / Crankshaft ratio")
                $tr.append("th")
                    .attr("colspan", crankshaft_radiuses.length)
                    .text("Crankshaft radius")
            })

            $thead.append("tr").call(($tr) => {
                $tr.selectAll("th")
                    .data(crankshaft_radiuses)
                    .join("th")
                    .text((d) => d).call(() => {
                        $tr.insert("th", ":first-child")
                    })
            })
        })
        $table.append("tbody").call(($tbody) => {
            $tbody.selectAll("tr")
                .data(rod_scales)
                .join("tr")
                .each(function (rod_scale) {
                    d3.select(this).call(($tr) => {
                        $tr.append("th").text(rod_scale)
                        $tr.selectAll("td")
                            .data(crankshaft_radiuses)
                            .join("td").each(function (crankshaft_radius) {
                                new Engine(crankshaft_radius, crankshaft_radius * rod_scale, this).run()
                            })
                    })
                })
        })

    })
})
