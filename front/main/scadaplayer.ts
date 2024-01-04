import { Engine } from "../scadaplayer/engine"
import { parse_scada } from "../scadaplayer/parser"

const metadata = JSON.parse((document.getElementById("metadata")! as HTMLTextAreaElement).value)
const records = parse_scada((document.getElementById("scada")! as HTMLTextAreaElement).value)
const ui = new Engine(metadata, records)

ui.request_frame()
