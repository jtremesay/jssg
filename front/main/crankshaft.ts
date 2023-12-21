import * as d3 from "d3"

const PIN_RADIUS = 10
const PISTON_HEIGHT = PIN_RADIUS + 40
const PISTON_RADIUS = 50

class Engine {
    should_run: boolean

    crankshaft_radius: number
    rod_length: number

    crankshaft_node: d3.BaseType
    piston_node?: d3.BaseType
    rod_node?: d3.BaseType


    constructor(crankshaft_radius: number, rod_length: number, container: d3.BaseType) {
        this.should_run = true

        this.crankshaft_radius = crankshaft_radius
        this.rod_length = rod_length

        let width = 250//Math.max(PISTON_RADIUS, crankshaft_radius) * 2 + 50
        let height = 800//crankshaft_radius * 2 + rod_length + PISTON_HEIGHT + 50

        let $svg = d3.select(container)
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [-width / 2, -height + 150, width, height])
            .attr("style", "background-color: grey")

        this.crankshaft_node = $svg.append("g")
            .call(($crankshaft) => {
                $crankshaft.append("circle")
                    .attr("r", crankshaft_radius)
                    .attr("style", "fill: red")

                $crankshaft.append("g")
                    .attr("transform", [`translate(0, -${this.crankshaft_radius})`])
                    .call(($crankshaft_pin) => {
                        // rod
                        this.rod_node = $crankshaft_pin.append("g")
                            .call(($rod) => {
                                $rod.append("rect")
                                    .attr("x", -PIN_RADIUS)
                                    .attr("y", -this.rod_length)
                                    .attr("width", PIN_RADIUS * 2)
                                    .attr("height", rod_length)
                                    .attr("style", "fill: green")


                                // Piston
                                this.piston_node = $rod.append("g").call(($piston) => {
                                    $piston.append("rect")
                                        .attr("x", -PISTON_RADIUS)
                                        .attr("y", -PISTON_HEIGHT)
                                        .attr("width", PISTON_RADIUS * 2)
                                        .attr("height", PISTON_HEIGHT)
                                        .attr("style", "fill: blue")


                                    $piston.append("circle")
                                        .attr("r", PIN_RADIUS)
                                        .attr("style", "fill: pink")
                                }).node()
                            }).node()

                        $crankshaft_pin.append("circle")
                            .attr("r", PIN_RADIUS)
                            .attr("style", "fill: pink")
                    })
            }).node()
    }

    update(dt: DOMHighResTimeStamp) {
        dt /= 1000

        let theta = dt

        // Crankshaft
        d3.select(this.crankshaft_node)
            .attr("transform", [`rotate(${theta * 180 / Math.PI})`])
        // Rod
        d3.select(this.rod_node!)
            .attr("transform", [
                `rotate(${-theta * 180 / Math.PI})`,
                `rotate(${-(Math.asin(Math.sin(theta) * this.crankshaft_radius / this.rod_length)) * 180 / Math.PI})`,
            ])
        // Piston
        d3.select(this.piston_node!)
            .attr("transform", [
                `translate(0, ${-this.rod_length})`,
                `rotate(${(Math.asin(Math.sin(theta) * this.crankshaft_radius / this.rod_length)) * 180 / Math.PI})`,
            ])
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
    let rod_lengths = [40, 100, 150, 200, 250, 300]

    $app.append("table").call(($table) => {
        $table.append("thead").call(($thead) => {
            $thead.append("tr").call(($tr) => {
                $tr.append("th").text("Rod length")
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
                .data(rod_lengths)
                .join("tr")
                .each(function (rod_length) {
                    d3.select(this).call(($tr) => {
                        $tr.append("th").text(rod_length)
                        $tr.selectAll("td")
                            .data(crankshaft_radiuses)
                            .join("td").each(function (crankshaft_radius) {
                                new Engine(crankshaft_radius, rod_length, this).run()
                            })
                    })
                })
        })

    })
})
