# E1 pre-registration (written 2026-11-02T21:30Z, before any model call)

Predictions:
- E1a (Mast advocate): Mast scores highest on zero-shot generation.
- E1b (brief): CF best on structure/identity questions (S); Mast best on spacing questions (P).
- E1c (brief): Mast least drift (closed vocabulary); CF vs Lumos open, CF's biggest risk.
- Mine, stated before running: E1a Mast lowest, not highest (Mast is the least-documented of the three on the public web, so its prior should be weakest); CF highest on E1a. E1b: Lumos best on G (only fixture with a card-title identity class). E1c: CF drifts more than Lumos because its hyphen/underscore split leaves more free choices.

Pre-registered files (sha256):
    79070f8272326fd0953c89a73584b5a541456d66e819e742094dd1b5ad3b62ba  fixtures/a.html
    928c2fbee0c40ea2cabd2e3679e4c78cc035bca3745e013887a96b679119b132  fixtures/b.html
    93e0cd613206036ba208ddb53e7bfdafdf599ca7cf64018713e19b4026399afc  fixtures/c.html
    75aea837c33af8d1286dfb4583ab9c3846eb9b9346b7afe82b22ecf2d6dd299c  fixtures/grammar-cf.txt
    436a6bb4ee3a47fff8b1ad409616d5b7661fec9413e4f22e99ad9e4f09753dbb  fixtures/grammar-lumos.txt
    64dcc912240a54adccfa92b226e7dbca8759e800fac7cae265009e35f50198e4  fixtures/grammar-mast.txt
    3ac96024938d6fb2d948a7674e8e7ca0580f3593651035f02bf21e5a92239708  scripts/e1a_key.py
    85917353a3af3b28047d79db55ddf5d44961a65e384533ba8f9a70b1ae54d082  scripts/e1b_key.py
    9bc9bbb52e4758304a3d30895054245dbd8aac28d96642a1c4b12d3886d12e3e  scripts/vocab.py
