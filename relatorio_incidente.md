# Relatório de Incidente de Segurança

**Total de tentativas falhas analisadas:** 5

### **Relatório de Análise de Incidente de Segurança - SOC**

**Classificação:** Alta / Movimentação Lateral Suspeita  
**Data da Análise:** 10 de Janeiro  
**Serviço Afetado:** SSH (OpenSSH daemon)  

---

### **1. Diagnóstico do Evento e Identificação do Atacante**

* **Isso é um ataque de força bruta?**  
  **Sim.** Trata-se de uma tentativa clássica de ataque de **força bruta / dicionário** automatizado direcionado ao protocolo SSH. 
* **Endereço IP de Origem:** `192.168.1.100`  
  *(**Atenção de SOC:** Por ser um IP privado RFC 1918, este tráfego indica uma ameaça interna, um teste de invasão não anunciado ou, mais criticamente, **movimentação lateral** originada de um host já comprometido na rede local).*

---

### **2. Recomendações Imediatas de Contenção**

1. **Bloqueio no Host Local (Host-based Firewall):**
   * Bloquear imediatamente o IP no firewall da máquina-alvo usando `iptables` ou `ufw`:
     ```bash
     # iptables
     sudo iptables -I INPUT -s 192.168.1.100 -j DROP

     # ou ufw
     sudo ufw insert 1 deny from 192.168.1.100
     ```
2. **Isolamento de Rede do Atacante:**
   * Localizar e isolar fisicamente ou via VLAN/Switch Port a máquina associada ao IP `192.168.1.100` para contenção e análise forense imediata.
3. **Mitigação a Médio Prazo no Servidor:**
   * Ativar ferramentas de prevenção de intrusão como o **Fail2ban**.
   * Desativar a autenticação SSH por senha (`PasswordAuthentication no`), impondo exclusivamente o uso de chaves públicas/privadas (SSH Keys).
   * Desabilitar login direto do usuário root (`PermitRootLogin no`).

---

### **3. Explicação Técnica do Ocorrido**

Durante o intervalo de 5 segundos (de 10:00:01 a 10:00:05), o servidor registrou conexões sequenciais provenientes do IP `192.168.1.100` em direção à porta padrão do SSH (22). 

* **Comportamento Automatizado:** As tentativas ocorreram a um ritmo exato de uma por segundo, com portas de origem incrementais (`54321` a `54325`), evidenciando o uso de um script/ferramenta automatizada de ataque (como Hydra, Medusa ou similar).
* **Varredura de Dicionário:** O atacante testou contas de alta prioridade e nomes padrão (`admin`, `root`, `test`).
* **Inexistência de Contas:** Todas as entradas registraram `Failed password for invalid user`, o que demonstra que a ferramenta não apenas errou as credenciais, mas também tentou contas que sequer existem cadastradas no sistema operacional (`invalid user`), reforçando o padrão de enumeração às cegas.