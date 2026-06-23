---
title: Immutable Infrastructure: Ein vollständiger Leitfaden
description: Eine Bereitstellungsphilosophie, bei der Server nach ihrer Bereitstellung niemals modifiziert werden, wodurch Konfigurationsdrift reduziert und Konsistenz über Umgebungen hinweg sichergestellt wird.
created: 2026-06-23
tags:
  - infrastructure
  - devops
  - deployment
  - cloud-computing
  - configuration-management
status: draft
---

# Immutable Infrastructure: Ein vollständiger Leitfaden

## Was ist Immutable Infrastructure?

Immutable Infrastructure ist ein Bereitstellungsmodell, bei dem Server oder Container **nach ihrer Bereitstellung niemals modifiziert werden**. Wenn ein Update erforderlich ist (ein Patch, eine Konfigurationsänderung oder eine Codeversion), wird die laufende Instanz zerstört und eine vollständig neue Instanz aus einem standardisierten, versionierten Artefakt erstellt – bezeichnet als „Golden Image“ oder Container-Image.

Dieser Ansatz steht im direkten Gegensatz zur **mutable Infrastructure** (veränderlichen Infrastruktur), der traditionellen Methode, bei der Administratoren per SSH auf laufende Server zugreifen, um Patches anzuwenden oder Konfigurationsmanagement-Tools (z. B. Ansible, Chef, Puppet) auszuführen. Mutable Infrastructure führt oft zu „Configuration Drift“ und „Snowflake Servern“ – Umgebungen, die mit der Zeit einzigartig und nicht reproduzierbar werden.

Immutable Infrastructure betrachtet Server als **Cattle, not Pets**: Sie sind austauschbar, nummeriert und leicht ersetzbar. Jede Änderung am System löst eine vollständige Neubereitstellung aus, anstatt eine Änderung vor Ort vorzunehmen.

## Warum Immutable Infrastructure?

Die Hauptmotivation für die Einführung von Immutable Infrastructure ist die Beseitigung von Configuration Drift und der dadurch verursachten Variabilität über Umgebungen hinweg. Zu den Vorteilen gehören:

- **Reproduzierbarkeit:** Jede Bereitstellung beginnt mit genau demselben Artefakt, was sicherstellt, dass Entwicklungs-, Staging- und Produktionsumgebungen identisch sind.
- **Einfachheit:** Rollbacks werden trivial – einfach die vorherige Image-Version erneut bereitstellen.
- **Sicherheit:** Für Produktionsinstanzen ist kein SSH-Zugriff erforderlich, was die Angriffsfläche reduziert. Audit-Trails sind klar: Welches Image wann ausgeführt wurde.
- **Skalierung:** Auto-Scaling-Gruppen oder Orchestratoren (z. B. Kubernetes) können neue Instanzen aus einem bekannten, guten Image starten und so sicherstellen, dass alle Knoten einheitlich sind.
- **Wegwerfbarkeit:** Instanzen können beendet und ersetzt werden, ohne die Verfügbarkeit zu beeinträchtigen, was nahtlose Blue/Green- und Canary-Deployments ermöglicht.

## Schlüsselprinzipien und -eigenschaften

| Prinzip | Beschreibung |
|---------|--------------|
| **Reproduzierbarkeit** | Jede Umgebung stammt aus demselben versionierten Artefakt. |
| **Wegwerfbarkeit** | Instanzen sind Vieh (Cattle) – sie können nach Belieben zerstört und neu erstellt werden. |
| **Atomare Bereitstellungen** | Updates erfolgen durch Austausch ganzer Stacks, niemals durch Patchen vor Ort. |
| **Vereinfachte Rollbacks** | Eine Rückkehr zu einem vorherigen Zustand bedeutet, das alte Artefakt erneut bereitzustellen. |
| **Idempotenz** | Dasselbe Artefakt, mehrmals bereitgestellt, erzeugt identische Ergebnisse. |
| **Kein Live-Patching** | Konfigurationsmanagement wird nur während der Image-Erstellung angewendet, nicht zur Laufzeit. |

## Geschichte und Ursprünge

- **2012 – „Pets vs. Cattle“:** Diese Analogie wurde von Randy Bias (CloudScaling) und Bill Baker (Microsoft) populär gemacht. Pets (Haustiere) sind einzigartig und werden manuell gepflegt; Cattle (Vieh) sind nummeriert, standardisiert und leicht ersetzbar.
- **2013 – Chad Fowlers Blogbeitrag „Immutable Infrastructure“** definierte den Begriff formal.
- **2013 – Docker Launch:** Container wurden zum perfekten Vehikel für Unveränderlichkeit – flüchtig, standardisiert, aus Images erstellt.
- **2014 – HashiCorp Packer:** Machte es praktikabel, identische Maschinenimages für mehrere Cloud-Anbieter (AWS AMI, Azure VHD, VMware) aus einer einzigen Vorlage zu erstellen.
- **2015–Gegenwart – Kubernetes, Terraform, CI/CD-Pipelines:** Diese Tools haben immutable Deployments zum Industriestandard für Cloud-native Anwendungen gemacht.

## Tooling-Ökosystem

Immutable Infrastructure ist ein **Paradigma**, kein einzelnes Softwarepaket. Die folgende Tabelle zeigt die wichtigsten Tools und deren Installation.

| Ebene | Werkzeug | Installation | Zweck |
|-------|----------|--------------|-------|
| **Image Builder** | HashiCorp Packer | `brew install packer` / Download binary | Golden VMs/AMIs erstellen |
| **Container Image** | Docker / Podman | `brew install docker` / `apt install docker.io` | Container-Images erstellen |
| **Image Registry** | Docker Hub / ECR / GCR | Cloud provider console / CLI setup | Unveränderliche Artefakte speichern und versionieren |
| **IaC / Orchestrierung** | Terraform / Pulumi / Kubernetes | `brew install terraform` / `kubectl` | Unveränderliche Ressourcen bereitstellen |
| **CI/CD** | GitLab CI / GitHub Actions | Configure runners | Build und Deployment automatisieren |
| **Secrets Injection** | HashiCorp Vault / AWS Secrets Manager | Install Vault agent or CSI driver | Secrets zur Bootzeit injizieren, nicht beim Backen |

> **Hinweis:** Traditionelle Konfigurationsmanagement-Tools (Ansible, Chef, Puppet) spielen immer noch eine Rolle, jedoch nur **während der Image-Build-Phase** – innerhalb eines Packer Provisioners oder Dockerfiles, niemals gegen laufende Produktionsinstanzen.

## Einfaches Anwendungsbeispiel

Lassen Sie uns einen typischen Arbeitsablauf durchgehen: Bereitstellung eines Nginx-Webservers auf AWS unter Verwendung von Immutable-Prinzipien.

### Schritt 1: Golden Image mit Packer erstellen

Erstellen Sie eine Packer-Vorlage, z. B. `web.pkr.hcl`:

```hcl
# web.pkr.hcl
source "amazon-ebs" "web" {
  ami_name      = "nginx-web-{{timestamp}}"
  source_ami    = "ami-0c02fb55956c7d316"   # Ubuntu 22.04 LTS
  instance_type = "t2.micro"
  region        = "us-east-1"
  ssh_username  = "ubuntu"
}

build {
  sources = ["source.amazon-ebs.web"]

  provisioner "shell" {
    inline = [
      "sudo apt-get update -y",
      "sudo apt-get install nginx -y",
      "sudo systemctl enable nginx"
    ]
  }
}
```

Erstellen Sie das Image:

```bash
packer build web.pkr.hcl
```

Die Ausgabe ist eine eindeutige AMI-ID, z. B. `ami-0abc123def456`. Dies wird das unveränderliche Artefakt.

### Schritt 2: Instanzen aus dem unveränderlichen Image bereitstellen

Verwenden Sie Terraform (`main.tf`):

```hcl
# main.tf
resource "aws_instance" "web" {
  ami           = "ami-0abc123def456"
  instance_type = "t2.micro"

  tags = {
    Name = "immutable-web-v1"
  }
}
```

Wenden Sie die Konfiguration an:

```bash
terraform apply
```

Eine einzelne EC2-Instanz wird aus dem goldenen AMI gestartet. Wenn sie ausfällt, wird eine neue aus demselben Image erstellt – kein Drift.

### Schritt 3: Ausrollen einer neuen Version

1. Aktualisieren Sie die Packer-Vorlage (z. B. eine neuere Nginx-Version installieren, aktualisierte statische Dateien kopieren).
2. Führen Sie `packer build` aus, um ein **neues** AMI zu erstellen: `ami-0new123ghi789`.
3. Ändern Sie das Feld `ami` in `main.tf` auf `ami-0new123ghi789`.
4. Führen Sie `terraform apply` aus. Terraform wird die alte Instanz zerstören und eine neue aus dem neuen Image erstellen.

**Keine Instanz wird jemals vor Ort gepatcht.** Jede Änderung ist ein vollständiger Austausch.

### Schritt 4: Blue/Green-Deployment (Produktionsmuster)

Für Updates mit Null-Ausfallzeit definieren Sie zwei separate Auto Scaling Groups (ASGs) oder Launch-Vorlagen in Terraform:

- **Blue** = aktuelle Version (v1)
- **Green** = neue Version (v2)

Nach der Bereitstellung der Green-ASG führen Sie Health Checks durch, wechseln dann die Zielgruppe des Application Load Balancers (ALB) von Blue zu Green. Sobald der Datenverkehr stabil ist, beenden Sie die Blue-ASG.

## Herausforderungen und Anti-Patterns

- **Mutable State (Veränderlicher Zustand):** Datenbanken und andere zustandsbehaftete Systeme können nicht als vollständig unveränderlich behandelt werden. Der Zustand muss außerhalb der Compute-Ebene isoliert werden (z. B. RDS, EBS-Volumes mit Snapshots oder Kubernetes StatefulSets mit Persistent Volume Claims).
- **Boot-Zeit:** Das Erstellen eines vollständigen OS-Images dauert länger als ein Hot Patch. Container reduzieren dies drastisch, aber große VM-Images können immer noch umständlich sein.
- **Image-Größe:** Ohne Disziplin (Multi-Stage-Docker-Builds, Bereinigungsskripte) werden Images aufgebläht und langsam bereitgestellt.
- **Debugging:** Ohne SSH-Zugriff basiert das Debuggen vollständig auf strukturiertem Logging (ELK, CloudWatch, Loki) und verteiltem Tracing (OpenTelemetry).
- **Secrets Management:** Secrets dürfen niemals in Images eingebacken werden. Sie müssen zur Boot-Zeit über Vault, AWS Secrets Manager oder CSI-Treiber injiziert werden.

## Fazit

Immutable Infrastructure verlagert die Betriebskomplexität **nach links** – in die Build-Pipeline – anstatt sie reaktiv in der Produktion zu verwalten. Während es eine anfängliche Investition in CI/CD und Tooling (Packer, Terraform, Kubernetes) erfordert, eliminiert es ganze Klassen von Ausfällen, die durch Configuration Drift und Umgebungsinkonsistenzen verursacht werden. Es ist das Fundament moderner Cloud-native Operationen und eine Voraussetzung für zuverlässige, sichere und skalierbare Microservices-Architekturen.