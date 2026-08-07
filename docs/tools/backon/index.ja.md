---
title: "backon: Python Retry Kütüphanesi"
description: "backon, yapı?landırılabilir backoff stratejileri kullanarak başarısız işlemleri otomatik olarak yeniden deneyen modern bir Python kütüphanesidir. Backoff'tan çatallanmıştır."
created: 2026-08-07
tags:
  - python
  - retry
  - backoff
  - resilience
status: draft
---

# back-on

`back-on` (pip: `backon`), kodunuza yeniden deneme mantığı eklemeyi basitleştiren bir Python kütüphanesidir. İyi bilinen [`backoff`](https://github.com/litaceans/backoff) kütüphanesinin bir çatalı olup, daha ifadesel, zincirlenebilir bir API ve modern Python (3.8+) desteği ile yeniden kurgulanmıştır. `back-on` sayesinde ağ çağrıları, veritabanı işlemleri, dosya G/Ç veya herhangi bir tutarsız (flaky) fonksiyonlardaki geçici hataları, temiz bir dekoratör veya bağlam yöneticisi sözdizimi ile kolayca ele alabilirsiniz.

## Neden back-on Kullanmalıyım?

- **Ergonomik** – Açık döngüler veya koşul kontrolleri yazmanıza gerek yok; tek bir dekoratör minimum kodla yeniden deneme davranışını içine yerleştirir.
- **Yapılandırılan stratejiler** – Sabit gecikmeler, üstel büyüme, tam veya ilişkili jitter (karışım) ile (thundering herd) etkisinden kaçınma.
- **Asenkron desteği** – `asyncio` ile doğal entegrasyon sağlayarak, olay döngüsünü bloklamadan asenkron kodda yeniden deneme yapılmasına olanak tanır.
- **Bildirim yaprakları** – Her yeniden deneme denemesinde ve pes edildikçe log veya metrik yayınlayın.
- **Sıfır bağımlılık** – Harici paket gerektirmeden hazır çalışır.

## Kurulum

pip ile kurun:

```bash
pip install backon
```

Proje yönetim stilinize göre `pyproject.toml` veya `requirements.txt` dosyasına da ekleyebilirsiniz.

## Temel Kullanım

`back-on`'un çekirdeği `@backon.on_exception` dekorid ağını içerir. Belirtilen istisnaları yakalar, hesaplanan gecikmeyi bekler ve süslenmiş fonksiyonu başarılı olana veya maksimum yeniden deneme süresine ulaşana kadar yeniden dener.

```python
import backon
import requests

@backon.on_exception(
    backoff.expo,
    requests.exceptions.RequestException,
    max_tries=8,
    max_time=30
)
def fetch_data(url):
    """Fetch a URL, retrying on any request error."""
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()
```

Yukarıdaki örnekte yazılım, en fazla 8 kez çağrılacak ve denemeler arası gecikme üstel geri çekilme (exponential backoff) kullanılarak hesaplanır (0.1 saniye başlayıp her denemede iki katına çıkar). Tüm denemelerde harcanan toplam süre 30 saniyeyi aşmayacaktır.

## Ana Özellikler

### 1. Çoklu Backoff Stratejileri

`back-on`, aşagıdaki yerleşik geri çekilme üreteçlerini sağlar:

| Strateji            | Açıklama                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `expo`              | Üstel geri çekilme: `base * 2^n`, burada `n` yeniden deneme sayısıdır. |
| `fib`               | Fibonacci tabanlı gecikmeler (gecikmeler önceki iki sayının toplamıyla artar). |
| `full_jitter`       | 0 ile mevcut üstel geri çekilme değeri arasındaki belirsiz gecikme. |
| `equal_jitter`      | Geri çekilme değerini rastgele bir parça ile sabit bir parça arasında böler. |
| `constant`          | Yeniden denemeler arasında sabit gecikme. |
| `decorrelated_jitter` | Tamamen rastgele olmayan, çakışmayı (contention) azaltan, ilişkilendirilmiş geri çekilme. |

İçe aktarırken şu sabitleri kullanın:

```python
from backon import expo, fib, full_jitter
```

### 2. Başarı veya İstisna Üzerine Yeniden Deneme

Varsayılan olarak `on_exception`, fonksiyon **raise** ettiğinde (belirlenmiş bir istisna) yeniden dener. Ayrıca `on_predicate` kullanarak fonksiyon özel bir değer veya nesne döndürdüğünde de yeniden deneyebilirsiniz:

```python
import backon

@backon.on_predicate(
    wait_gen=expo,
    predicate=lambda x: x is None,
    max_tries=5
)
def maybe_none():
    # ... may return None, which we treat as failure
    return None if random.random() < 0.7 else "OK"
```

### 3. Async Desteği

`back-on`, `asyncio` ile sorunsuz çalışır:

```python
import asyncio
import backon

@backon.on_exception(
    wait_gen=full_jitter,
    exception=TimeoutError,
    max_tries=3
)
async def flaky_async():
    # ... an async operation that sometimes times out
    await asyncio.sleep(0.1)
    class TimeoutError(Exception): pass
    raise TimeoutError()

async def main():
    await flaky_async()
```

Ayrı dekoratörlere gerek yoktur; kütüphane `async` fonksiyonlarını algılar ve arka planda `asyncio.sleep` kullanır.

### 4. Başarısızlıkta Bildirim

Yeniden denemeleri izlemek için `on_success`, `on_retry` ve `on_giveup` isteğine bağlı işlevler geçebilirsiniz:

```python
import logging
import backon

logging.basicConfig(level=logging.INFO)

@backon.on_exception(
    wait_gen=backon.expo,
    max_tries=5,
    on_retry=lambda exc, wait, tries: logging.warning(
        "Attempt %d failed with %s. Retrying in %.2f s", tries, exc, wait
    ),
    on_giveup=lambda exc, tries: logging.error("Giving up after %d", tries)
)
def service_call():
    # ...
    pass
```

`on_retry` işlemi, istisna örneğini, bekleme süresini (saniye), ve deneme sayısını alır. `on_giveup`, maksimum yeniden deneme sayısına ulaşıldıkmda çağırılır.

### 5. Özel Bekleme Üreteçleri

Geçeniz, geri çekilme sekansını saniye değerleri üreten bir jeneratör geçerek özelleştirebilirsiniz:

```python
def custom_delays():
    for d in [0.1, 0.2, 0.5, 1.0, 2.0]:
        yield d
```

Ardından `wait_gen=custom_delays` kullanarak yerleşik `backon.on_exception` ile birlikte kullanabilirsiniz. Dikkat edin, jeneratörün sonsuz olması gerekmektedir, çünkü dekoratör ihtiyaç oldukça değerler isteyecektir.

## Kullanım Örnekleri

### HTTP Istemcisi Üstel Geri Çekilme ile

```python
import requests
import backon

@backon.on_exception(
    backoff.expo,
    requests.exceptions.ConnectionError,
    max_tries=5,
    base=1,      # Başlangıçta 1 saniye
    factor=2.0   # Her denemede iki katı
)
def download(url: str) -> bytes:
    r = requests.get(url, timeout=3)
    r.raise_for_status()
    return r.content
```

### Veritabanı Bağlantısı

```python
import sqlite3
import backon

@backon.on_exception(
    wait_gen=backon.expo,
    exception=sqlite3.OperationalError,
    max_time=30
)
def get_connection(path: str) -> sqlite3.Connection:
    con = sqlite3.connect(path)
    # Bazen "database is locked" (veritabanı kilitli) hatası oluşabilir
    return con
```

`sleep_on` dekoratöründe `exception` belirtilmezse, tüm istisnaları dolaylı olarak yakalar – dikkatli istisna işleme ile kullanın.

## Gelişmiş: Async Generator Desteği (Python 3.8+)

`back-on`, asenkron üreteç fonkiyonlarında da çalışır:

```python
import backon
import asyncio

@backon.on_exception(
    backon.expo,
    RuntimeError,
    max_tries=5
)
async def async_gen():
    for i in range(10):
        yield i
```

Üreteci, her `__anext__` çağrısına yeniden deneme mantığı uygulayarak yineler; şayet üreteç bir istisna fırlatırsa, yeniden başlatılır. Bu, bir üretecin ortasında hata verebildiği durumlarda kullanışlıdır.

## Tip İpuçları ile Entegrasyon

Özel tip ipuçları gerekmez; hatalı istisna adları çalışma zamanında yakalanır. Kütüphane tamamen tipkaçı (typed) olduğundan, editörünüz öneriler sunabilir.

## `backoff` ile Karşılaştırma

| Özellik | `backoff` (orijinal) | `back-on` |
|------------------------------------------------|:--------------------:|:---------------------------:|
| Dekoratör sözdizimi | `@backoff.on_exception` gerektirir | Aynı, ancak zincirilebilir yöntemler mevcut |
| `on_success` kancası                            | ❌                    | ✅                          |
| Async desteği                                   | ✅ ancak ayrı dekoratör | ✅ birleşik (tek) dekoratör |
| Esnek bekleme tablosu                           | ✅                    | ✅ – hepsi hala mevcut              |
| Tip ipuçları                                   | Kısmi                | Kapsamlı                     |
| Proje etkinliği                                   | Bakımda               | Aktif geliştirme             |

## Sonuç

`back-on`, `backoff` için mevcut her şeyi koruyup basitliğini muhafaza ederken modern ergonomikler ekleyen, üzerine eldiven gibi oturan (drop-in) bir değiştirmedir. Python betiklerinizin geçici dalga hatlarına dayanıklılığını arttıracak güvenilir ve kolay bir çözüm arıyorsanız, `back-on`'ı deneyin.

```bash
pip install backon
```

Mutlu ve dayanıklı kodlamalar!