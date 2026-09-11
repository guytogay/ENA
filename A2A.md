# Agent-to-Agent communication

ENA expects a practical two-way path to at least one other Agent when the Host can support it. Reuse a working Host-native or standards-based A2A implementation when one already exists.

## If A2A already exists

1. Find the Agent Card or discovery record used by the implementation.
2. Verify the advertised endpoint, capabilities and authentication requirements against reality.
3. Complete a real two-way exchange with another Agent.
4. Save stable references in `ENA.yaml`.

Do not create a second ENA identity system when the A2A implementation already provides identity/discovery.

## If A2A does not exist

When the Host provides enough capability to create it:

1. choose the simplest reliable implementation appropriate to the Host;
2. expose/register the Agent using that implementation's normal discovery mechanism;
3. configure authentication and authorization without writing plaintext secrets into ENA records;
4. establish at least one reachable peer;
5. prove a real two-way exchange works;
6. save stable references in `ENA.yaml`.

## Keep at least one rescue peer

For a risky self-change, another Agent should be able to receive the recovery package before live state is modified.

The rescue peer should be able to:

- receive `rescue.yaml` and the location of required recovery material;
- acknowledge the exact change package before the change starts;
- reach the target Host or recovery mechanism when authorized;
- determine whether communication has returned;
- follow the prepared rollback without first reconstructing the target Agent from conversation history.

If the peer can receive messages but cannot actually execute or relay recovery, record that limitation instead of treating delivery alone as rescue capability.

## Protect the rescue path

Changes to networking, authentication, routing, startup or the A2A endpoint can remove the same path needed for rescue.

For such changes:

- send the recovery package before modifying live state;
- keep automatic rollback outside the component being changed;
- avoid changing the only recovery channel and its only backup in the same operation;
- require a new real two-way exchange before retaining the change.

See `SAFE-CHANGE.md`.

## Configuration example

```yaml
communication:
  a2a:
    agent_card: https://agent.example.com/.well-known/agent-card.json
    rescue_peers:
      - agent_card: https://peer.example.com/.well-known/agent-card.json
        access: configured
```

Use the discovery form supported by the actual A2A implementation. Do not store credentials/private keys in `ENA.yaml` merely to make the reference self-contained.
