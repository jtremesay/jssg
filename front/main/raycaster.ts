import { Raycaster } from "../raycaster/engine";


function main() {
    let rc_node = document.getElementById("raycaster");
    if (rc_node == null) {
        return
    }
    let rc = new Raycaster(rc_node);
    rc.run();
}

main();