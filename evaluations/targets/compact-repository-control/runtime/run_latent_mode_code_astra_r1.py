#!/usr/bin/env python3
"""固定済み小規模A01を、モデルだけAstraへ変えて測定する。"""
import importlib.util
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('latent_original', BASE/'runtime/run_latent_mode_code_r1.py')
original = importlib.util.module_from_spec(spec)
spec.loader.exec_module(original)
original.PROFILE = BASE/'profiles/free-astra6-low-latent-mode-code-n2-r1.json'

if __name__ == '__main__':
    registration = original.runner.load(BASE/'registrations/latent-mode-code-astra-source-freeze-r1.json')
    for path, digest in registration['sha256'].items():
        if original.runner.sha(original.REPO/path) != digest:
            raise ValueError('Astra固定アーティファクト不一致: '+path)
    astra = original.runner.load(original.PROFILE)
    sol = original.runner.load(BASE/'profiles/free-sol61-low-latent-mode-code-n2-r1.json')
    for key in ['evaluation_set_ref','rating_ref','prompt_ref','repetition','budget']:
        if astra[key] != sol[key]:raise ValueError('モデル以外の条件不一致: '+key)
    ar=dict(astra['runtime']);sr=dict(sol['runtime']);ar.pop('model');sr.pop('model')
    if ar != sr:raise ValueError('モデル以外の実行条件不一致')
    campaign=Path(sys.argv[1]).resolve()
    original.runner.write(campaign/'model-axis-preflight.json',{'source_registration_sha256':original.runner.sha(BASE/'registrations/latent-mode-code-astra-source-freeze-r1.json'),'reference_result_sha256':original.runner.sha(BASE/'results/free-sol61-low-latent-mode-code-n2_2026-10-01.json'),'declared_axis':'runtime.model','from':'gpt-6.1-sol','to':'gpt-6-astra','non_model_profile_fields_equal':True,'queue_policy':'独立二回を順次実行','prompt_comparison':False})
    original.main()
