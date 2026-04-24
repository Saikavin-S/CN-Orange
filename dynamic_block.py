from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

mac_to_port = {}
packet_count = {}
blocked_hosts = set()

THRESHOLD = 20


def _handle_PacketIn(event):
    packet = event.parsed
    src = packet.src
    dst = packet.dst
    in_port = event.port

    mac_to_port[src] = in_port

    packet_count[src] = packet_count.get(src, 0) + 1

    if packet_count[src] > THRESHOLD and src not in blocked_hosts:
        log.info("Blocking Host: %s", src)
        blocked_hosts.add(src)
        msg = of.ofp_flow_mod()
        msg.match.dl_src = src
        event.connection.send(msg)
        return

    if dst in mac_to_port:
        out_port = mac_to_port[dst]
    else:
        out_port = of.OFPP_FLOOD

    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=out_port))
    event.connection.send(msg)


def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("Dynamic Host Blocking Controller Started")
