function create_triangles(deep: number) {
    if (deep == 0) {
        const path = document.createElementNS("http://www.w3.org/2000/svg", "path")
        path.setAttribute("d", `M 0.5,0L${0.5 - Math.sin(Math.PI / 3) / 2},0.75 ${0.5 + Math.sin(Math.PI / 3) / 2},0.75Z`)
        path.setAttribute("fill", "yellow")
        path.classList.add("triangle")
        return path
    }

    const g = document.createElementNS("http://www.w3.org/2000/svg", "g")
    g.classList.add("triangle")

    const triangle_a = create_triangles(deep - 1)
    triangle_a.setAttribute("transform", `scale(0.5, 0.5) translate(0.5, 0)`)
    g.appendChild(triangle_a)

    const triangle_b = create_triangles(deep - 1)
    triangle_b.setAttribute("transform", `scale(0.5, 0.5) translate(${0.5 - Math.sin(Math.PI / 3) / 2}, 0.75)`)
    g.appendChild(triangle_b)

    const triangle_c = create_triangles(deep - 1)
    triangle_c.setAttribute("transform", `scale(0.5, 0.5) translate(${0.5 + Math.sin(Math.PI / 3) / 2}, 0.75)`)
    g.appendChild(triangle_c)

    return g
}

function sierpinski(svg: SVGElement) {
    const input = document.getElementById(svg.dataset.sierpinskiInput ?? "sierpinski-input") as HTMLInputElement
    if (input !== null) {
        input.addEventListener("input", (event) => {
            svg.querySelectorAll(".triangle").forEach((triangles) => triangles.remove())
            svg.appendChild(create_triangles(parseInt((event.target as HTMLInputElement).value)))
        })
        svg.appendChild(create_triangles(parseInt(input.value)))
    } else {
        svg.appendChild(create_triangles(1))
    }
}

document.querySelectorAll("svg.sierpinski").forEach((svg) => sierpinski(svg as SVGElement))