# Dynamic Host Blocking System using SDN

## 1. Problem Statement

Suspicious hosts can disrupt a network by flooding traffic. Traditional networks cannot respond dynamically. This project uses an SDN controller to detect and block such hosts automatically using OpenFlow rules.

---

## 2. Objective

- Monitor all traffic through a POX SDN controller
- Count packets per host
- Block any host that exceeds 20 packets
- Allow normal hosts to communicate without interruption

---

## 3. Tools & Technologies Used

- **Mininet** – Network emulator
- **POX Controller** – SDN controller
- **OpenFlow Protocol** – Switch-controller communication
- **Python** – Controller implementation
- **Ubuntu Linux** – Development environment

---

## 4. Network Topology

```
h1 ----\
        s1 ---- POX Controller
h2 ----/
h3 ----/

h1 = Normal host
h2 = Normal host
h3 = Attacker
```

---

## 5. Working Principle

1. Every unmatched packet is sent from the switch to the controller via **PacketIn**
2. Controller learns which port each MAC address is on
3. Controller counts how many packets each host has sent
4. If a host exceeds **20 packets**, a DROP flow rule is installed on the switch
5. All future packets from that host are dropped at the switch level
6. Other hosts continue to communicate normally

---

## 6. Controller Logic

| Part | Purpose |
|---|---|
| `mac_to_port` | Maps each MAC address to its switch port |
| `packet_count` | Counts total packets received from each MAC |
| `blocked_hosts` | Stores MACs that have been blocked |
| `THRESHOLD = 20` | Max packets allowed before a host is blocked |
| `_handle_PacketIn` | Main function — learns MAC, counts packets, blocks or forwards |
| `launch` | POX entry point — registers the PacketIn listener |

---

## 7. Steps to Run

### Step 1: Copy controller to POX

```bash
cp dynamic_block.py ~/pox/ext/
```

### Step 2: Start POX Controller

```bash
cd ~/pox
./pox.py openflow.of_01 ext.dynamic_block
```

### Step 3: Start Mininet (new terminal)

```bash
sudo mn --topo single,3 --controller remote --switch ovsk,protocols=OpenFlow10
```

---

## 8. Test Scenarios

### Scenario 1 — Normal Traffic (ALLOWED)

```
mininet> h1 ping -c 3 h2
```

Expected:
```
0% packet loss
```

### Scenario 2 — Flood Attack (BLOCKED)

```
mininet> h3 ping -f h1
```

Controller log:
```
Blocking Host: 00:00:00:00:00:03
```

### Scenario 3 — Verify Block

```
mininet> h3 ping -c 5 h1
```

Expected:
```
100% packet loss
```

---

## 9. Flow Table Verification

```
mininet> dpctl dump-flows
```

Expected:
```
dl_src=00:00:00:00:00:03 actions=drop
```

---

## 10. Performance Measurement

### Latency

```
mininet> h1 ping -c 10 h2
```

### Throughput

```
mininet> h2 iperf -s &
mininet> h1 iperf -c h2 -t 5
```

---

## 11. Results

- Normal traffic forwarded successfully
- Suspicious host blocked after exceeding threshold
- DROP rule visible in flow table
- Normal hosts unaffected after blocking

---

## 12. Conclusion

This project demonstrates how SDN enables real-time, centralized traffic control. The POX controller dynamically detects misbehaving hosts and enforces blocking rules on the switch instantly — without any manual intervention.

---

## 13. References

- https://mininet.org
- https://github.com/noxrepo/pox
- https://opennetworking.org
