# ENA A2A

Status: working draft — not Current.

ENA uses A2A as the Agent's practical path to other Agents for collaboration and rescue. Reuse a working Host-native or standards-based A2A implementation when one already exists.

## During First Use

Determine whether the Agent already has a real bidirectional A2A path.

If A2A already exists:

1. find the Agent Card or other standard discovery record used by that A2A implementation;
2. verify that its advertised endpoint, capabilities, authentication requirements, and reachable identity match reality;
3. complete a real two-way exchange with at least one other Agent;
4. store the stable Agent Card reference and useful peer references in `ENA.yaml`.

If A2A does not exist and the Host gives the Agent enough capability to create it:

1. choose the simplest reliable A2A implementation appropriate to the Host;
2. expose or register the Agent using the A2A identity/discovery mechanism in use;
3. configure authentication and authorization without placing plaintext secrets in ENA records or Agent Cards;
4. establish at least one reachable peer;
5. prove a real bidirectional exchange works;
6. persist the stable references in `ENA.yaml`.

Do not create a separate ENA identity system when the A2A implementation already supplies Agent identity and discovery.

## Keep a rescue peer

For ACMS protected changes, the changing Agent needs at least one other Agent that can receive the rescue package before the change is applied.

A rescue peer should be able to:

- receive the change's `rescue.yaml` and the location of any required recovery material;
- acknowledge receipt before the body-changing operation starts;
- reach the target Host or the recovery mechanism when authorized to act;
- determine whether the target Agent has recovered through a normal bidirectional exchange;
- follow the prepared rollback path without first reconstructing the target Agent's architecture.

The peer does not need to be a permanent controller of the target Agent. It is an external recovery path and collaborator.

## Do not assume receipt

Sending a rescue package is not enough. Before ACMS applies the protected change, obtain an explicit acknowledgement from the selected peer that identifies the same change package.

The acknowledgement should be durable enough that the changing Agent can record:

- which peer received it;
- which change package was acknowledged;
- when it was acknowledged, using the canonical timezone;
- whether the peer has the access required to execute the prepared rescue path.

If no peer can actually perform or relay recovery, record that limitation rather than treating message delivery alone as rescue capability.

## Keep A2A usable after change

A body-changing operation that affects A2A, networking, authentication, routing, runtime startup, or the Agent Card is especially dangerous because it can remove the same channel used for rescue.

For such changes:

- send the rescue package before mutation;
- keep the automatic rollback mechanism outside the modified failure surface;
- avoid changing the only recovery path and its only backup at the same time;
- after the change, require a new real bidirectional exchange before ACMS retains the change.

## ENA configuration

`ENA.yaml` may keep stable A2A references such as:

```yaml
a2a:
  agent_card: https://agent.example.com/.well-known/agent-card.json
  rescue_peers:
    - agent_card: https://peer.example.com/.well-known/agent-card.json
      access: configured
```

Use the actual discovery form supported by the A2A implementation. Do not embed credentials or private keys in `ENA.yaml` merely to make the reference self-contained.
