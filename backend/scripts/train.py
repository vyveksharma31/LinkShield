"""Reproducible Machine Learning Training Pipeline for LinkShield.

Curates a benchmark training corpus, extracts 30 static lexical/structural features,
trains a regularized Random Forest classifier, evaluates classification metrics,
and serializes the trained model bundle to backend/models/phishing_rf_v1.joblib.
"""
import os
import sys
import json
from datetime import datetime, timezone
from pathlib import Path

# Ensure LinkShield backend is in python path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split

from backend.app.engine.parser import normalize_and_parse_url
from backend.app.engine.features import extract_features, features_to_vector, ML_FEATURE_NAMES


# Curated benchmark dataset of legitimate URLs (label = 0)
LEGITIMATE_URLS = [
    "https://www.google.com/search?q=cybersecurity+threat+intelligence",
    "https://github.com/vyveksharma31/LinkShield",
    "https://en.wikipedia.org/wiki/Phishing",
    "https://apple.com/macbook-pro",
    "https://microsoft.com/en-us/security/business",
    "https://aws.amazon.com/ec2/pricing/",
    "https://www.cloudflare.com/learning/security/what-is-zero-trust/",
    "https://stackoverflow.com/questions/tagged/fastapi",
    "https://developer.mozilla.org/en-US/docs/Web/Security",
    "https://fastapi.tiangolo.com/tutorial/bigger-applications/",
    "https://pypi.org/project/scikit-learn/",
    "https://docs.python.org/3/library/urllib.parse.html",
    "https://www.nytimes.com/section/technology",
    "https://www.bbc.com/news/technology",
    "https://reuters.com/business",
    "https://cnn.com/world",
    "https://harvard.edu/admissions",
    "https://mit.edu/research",
    "https://stanford.edu/academics",
    "https://berkeley.edu/departments",
    "https://ox.ac.uk/students",
    "https://cam.ac.uk/research",
    "https://nasa.gov/missions",
    "https://cdc.gov/flu",
    "https://who.int/emergencies",
    "https://nih.gov/health-information",
    "https://paypal.com/us/home",
    "https://chase.com/personal",
    "https://bankofamerica.com/smallbusiness",
    "https://wellsfargo.com/investing",
    "https://binance.com/en/trade",
    "https://coinbase.com/explore",
    "https://netflix.com/browse",
    "https://spotify.com/us/premium",
    "https://steamcommunity.com/discussions",
    "https://store.steampowered.com/toprated",
    "https://adobe.com/products/creativecloud.html",
    "https://dropbox.com/business",
    "https://slack.com/solutions",
    "https://zoom.us/pricing",
    "https://docker.com/products/docker-desktop",
    "https://postman.com/api-platform",
    "https://npmjs.com/package/react",
    "https://yarnpkg.com/features",
    "https://gitlab.com/explore",
    "https://bitbucket.org/product",
    "https://medium.com/tag/machine-learning",
    "https://dev.to/t/python",
    "https://news.ycombinator.com/",
    "https://reddit.com/r/netsec",
    "https://kernel.org/pub/linux/kernel",
    "https://archlinux.org/packages",
    "https://ubuntu.com/server",
    "https://debian.org/releases",
    "https://digitalocean.com/products/droplets",
    "https://linode.com/pricing",
    "https://salesforce.com/products",
    "https://shopify.com/online-store",
    "https://stripe.com/payments",
    "https://ebay.com/deals",
    "https://etsy.com/c/jewelry",
    "https://walmart.com/browse/electronics",
    "https://target.com/c/home",
    "https://ikea.com/us/en/",
    "https://homedepot.com/b/Appliances",
    "https://bestbuy.com/site/computers-tablets",
    "https://cisco.com/c/en/us/products/security",
    "https://paloaltonetworks.com/prisma",
    "https://fortinet.com/products/next-generation-firewall",
    "https://splunk.com/en_us/products/enterprise-security.html",
    "https://elastic.co/what-is/elasticsearch",
    "https://mongodb.com/products/platform/atlas-database",
    "https://postgresql.org/docs/current/",
    "https://redis.io/docs/about/",
    "https://apache.org/licenses/",
    "https://freebsd.org/releases/",
    "https://cve.org/About/Overview",
    "https://nvd.nist.gov/vuln",
    "https://owasp.org/www-project-top-ten/",
    "https://sans.org/cyber-security-courses/",
]

# Curated benchmark dataset of phishing and malicious URLs (label = 1)
PHISHING_URLS = [
    # Brand Impersonation in Subdomains
    "https://paypal.secure-verification-portal.com/login",
    "https://paypal.account-update-alert.xyz/verify",
    "https://apple.id-support-recover-account.net/verify",
    "https://apple.icloud-unlock-portal.click/auth",
    "https://chase.online-banking-access.org/auth",
    "https://chase.verification-security.top/login",
    "https://microsoft.account-reset-pass.xyz/signin",
    "https://microsoft.office365-verify-portal.work/login",
    "https://netflix.billing-update-center.click/account",
    "https://netflix.payment-renewal-issue.tk/signin",
    "https://binance.wallet-validation-portal.com/security",
    "https://coinbase.pro-recovery-service.top/confirm",
    "https://amazon.order-cancellation-notice.work/review",
    "https://amazon.prime-security-check.gq/login",
    "https://google.account-security-alert.ml/signin",
    "https://bankofamerica.secure-mobile-session.xyz/auth",
    "https://wellsfargo.account-auth-center.cf/verify",
    "https://steam.community-gift-trade.club/login",
    "https://adobe.cloud-credential-check.top/portal",
    "https://dropbox.file-share-verify.buzz/signin",

    # Brand Impersonation in Path / Query
    "http://evil-tracker.com/paypal/signin/verify.php",
    "http://untrusted-host.net/service/apple/icloud-login",
    "http://phish-lab.xyz/auth?target=chase&action=login",
    "http://cdn-proxy.online/microsoft/office365/portal",
    "http://fake-gateway.org/wellsfargo/auth/index.html",
    "http://server-check.biz/binance/wallet/recover",
    "http://host-redirect.cc/amazon/signin.php?token=xyz",
    "http://cloud-redirect.top/google/drive/share?login=1",

    # IP Address Literal Hosts (IPv4, Hex, Octal, Dword)
    "http://192.168.1.1/admin/login",
    "http://192.168.1.100/chase/login",
    "http://10.0.0.1:8080/portal/auth",
    "http://172.16.254.1:8443/secure",
    "http://0x7f.0x00.0x00.0x01/login",
    "http://0177.0.0.1/verify",
    "http://2130706433/account",
    "http://192.168.10.50:9090/service?token=12345",
    "http://45.33.32.156/bank/signin.php",
    "http://185.220.101.5/paypal/verify",
    "http://194.26.29.112/office365/login",
    "http://91.240.118.88:8080/credential-harvest",

    # Credential Delimiter Tricks (@ symbol)
    "http://paypal.com@evil-attacker-site.com/login",
    "http://google.com@192.168.1.100/verify",
    "https://chase.com:welcome@banking-portal-fake.xyz/",
    "http://user:password@legit-looking.com.phish.org/auth",
    "http://appleid.apple.com@security-check-unlock.top/id",
    "http://microsoft.com@365-verify.club/signin",

    # Suspicious TLD Lures
    "http://account-alert.xyz/verify",
    "http://urgent-notice.top/banking",
    "http://free-gift-crypto.tk/claim",
    "http://system-validator.work/auth",
    "http://cloud-storage-file.click/download",
    "http://security-update-center.buzz/login",
    "http://easy-loan-approval.loan/apply",
    "http://banking-service-auth.fit/signin",
    "http://wallet-airdrop-claim.surf/connect",
    "http://paypal-resolution-center.country/dispute",

    # Excessive Subdomains & Nested Evasion
    "http://a.b.c.d.e.f.secure-bank.example.com/login",
    "https://portal.stage.dev.test.auth.internal-spoof.net/",
    "http://1.2.3.4.5.sub.evil.org/phish",
    "http://secure.login.verify.account.update.fake-auth.com/",
    "http://mobile.banking.service.auth.client.phish-net.org/",

    # Obfuscated Encoding & Lure Keywords
    "http://phish.net/page%20with%20spaces/index.html",
    "http://target.com/path%2e%2e%2fadmin%2fcredentials",
    "http://host.xyz/%70%61%79%70%61%6c/login",
    "http://portal.org/%61%70%70%6c%65/verify?auth=token",
    "http://evil.com/login/signin/verify/account/password/banking/confirm",

    # IDN Homoglyphs and Punycode
    "https://xn--pypal-4ve.com/signin",
    "https://xn--appl-43a.com/id",
    "https://xn--googl-r0a.com/search",
    "http://xn--chse-q5a.com/banking",
    "https://xn--microsft-e1a.com/office",

    # DGA & High Entropy Hosts
    "http://xkq9m2w8znv7b4p1.com/beacon",
    "http://7b9f3a2c8e1d5046.biz/gate.php",
    "http://zxcasdqwe123987456.cc/payload",
    "http://q981kzmna291048.info/drop",
    "http://mnbzvcxlasdqwe12.org/exfil",
]


def build_dataset() -> tuple[np.ndarray, np.ndarray]:
    """Extract features for the corpus and assemble feature matrix X and target y."""
    X_list = []
    y_list = []

    print(f"[*] Extracting features for {len(LEGITIMATE_URLS)} legitimate URLs...")
    for url in LEGITIMATE_URLS:
        try:
            parsed = normalize_and_parse_url(url)
            features = extract_features(parsed)
            vec = features_to_vector(features)
            X_list.append(vec)
            y_list.append(0)
        except Exception as e:
            print(f"[!] Warning: failed to parse legit URL {url}: {e}")

    print(f"[*] Extracting features for {len(PHISHING_URLS)} phishing URLs...")
    for url in PHISHING_URLS:
        try:
            parsed = normalize_and_parse_url(url)
            features = extract_features(parsed)
            vec = features_to_vector(features)
            X_list.append(vec)
            y_list.append(1)
        except Exception as e:
            print(f"[!] Warning: failed to parse phishing URL {url}: {e}")

    X = np.array(X_list, dtype=np.float32)
    y = np.array(y_list, dtype=np.int32)
    return X, y


def train_model() -> dict:
    """Train Random Forest classifier, evaluate metrics, and save serialized model artifact."""
    X, y = build_dataset()
    print(f"[*] Dataset assembled: {X.shape[0]} samples, {X.shape[1]} features.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    print(f"[*] Training Random Forest Classifier (100 estimators, max_depth=12)...")
    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=12,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=1,
    )
    clf.fit(X_train, y_train)

    # Evaluation
    y_pred = clf.predict(X_test)
    y_proba = clf.predict_proba(X_test)[:, 1]

    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, zero_division=0))
    rec = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    auc = float(roc_auc_score(y_test, y_proba))
    cm = confusion_matrix(y_test, y_pred).tolist()

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0

    print("=" * 60)
    print(" LINKSHIELD MODEL EVALUATION REPORT")
    print("=" * 60)
    print(f"  Accuracy:       {acc * 100:.2f}%")
    print(f"  Precision:      {prec * 100:.2f}%")
    print(f"  Recall:         {rec * 100:.2f}%")
    print(f"  F1 Score:       {f1 * 100:.2f}%")
    print(f"  ROC-AUC:        {auc:.4f}")
    print(f"  False Pos Rate: {fpr * 100:.2f}%")
    print(f"  Confusion Matrix: TN={tn}, FP={fp}, FN={fn}, TP={tp}")
    print("=" * 60)

    # Serialize model artifact
    models_dir = ROOT_DIR / "backend" / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / "phishing_rf_v1.joblib"

    metadata = {
        "model_version": "rf-v1.0",
        "algorithm": "RandomForestClassifier",
        "n_estimators": 100,
        "max_depth": 12,
        "features": ML_FEATURE_NAMES,
        "num_features": len(ML_FEATURE_NAMES),
        "metrics": {
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1_score": f1,
            "roc_auc": auc,
            "false_positive_rate": fpr,
            "confusion_matrix": cm,
        },
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "total_samples": int(X.shape[0]),
    }

    bundle = {
        "model": clf,
        "metadata": metadata,
    }

    import pickle
    with open(model_path, "wb") as f:
        pickle.dump(bundle, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"[OK] Model artifact saved to: {model_path}")

    # Also save metadata as human-readable JSON
    meta_path = models_dir / "model_metrics.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"[OK] Metrics JSON saved to: {meta_path}")

    return metadata


if __name__ == "__main__":
    train_model()
