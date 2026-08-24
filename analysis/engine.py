import pefile
from elftools.elf.elffile import ELFFile
import hashlib
import os
import yara
import logging
import json

logger = logging.getLogger(__name__)

def get_hashes(file_path: str):
    sha256 = hashlib.sha256()
    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
            md5.update(chunk)
    return sha256.hexdigest(), md5.hexdigest()

def analyze_pe(file_path: str):
    try:
        pe = pefile.PE(file_path)
        results = {
            "entry_point": hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint),
            "sections": [],
            "imports": [],
            "exports": []
        }
        for section in pe.sections:
            results["sections"].append({
                "name": section.Name.decode().strip('\x00'),
                "size": section.SizeOfRawData,
                "entropy": section.get_entropy()
            })
        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                for imp in entry.imports:
                    results["imports"].append({
                        "dll": entry.dll.decode(),
                        "name": imp.name.decode() if imp.name else None
                    })
        if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
            for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
                results["exports"].append({
                    "name": exp.name.decode() if exp.name else None,
                    "address": hex(exp.address)
                })
        return results
    except Exception as e:
        logger.error(f"Error analyzing PE: {e}")
        return {"error": str(e)}

def analyze_elf(file_path: str):
    try:
        with open(file_path, 'rb') as f:
            elffile = ELFFile(f)
            results = {
                "entry_point": hex(elffile.header['e_entry']),
                "sections": [],
                "architecture": elffile.get_machine_arch()
            }
            for section in elffile.iter_sections():
                results["sections"].append({
                    "name": section.name,
                    "size": section['sh_size'],
                    "type": section['sh_type']
                })
            return results
    except Exception as e:
        logger.error(f"Error analyzing ELF: {e}")
        return {"error": str(e)}

def run_yara(file_path: str):
    # For now, just a placeholder if no rules are provided
    # In a real scenario, we'd load rules from a directory
    return []

def run_capa(file_path: str):
    # capa integration is complex as it usually runs as a CLI or needs specific setup
    # We will provide a fault-tolerant placeholder
    return {"status": "Not implemented in MVP"}

def static_analysis_engine(file_path: str, file_type: str):
    sha256, md5 = get_hashes(file_path)
    
    report = {
        "sha256": sha256,
        "md5": md5,
        "file_size": os.path.getsize(file_path),
        "file_type": file_type,
        "metadata": {}
    }
    
    if "PE32" in file_type or "executable" in file_type: # Simple check for PE
        report["metadata"] = analyze_pe(file_path)
    elif "ELF" in file_type:
        report["metadata"] = analyze_elf(file_path)
    
    report["yara"] = run_yara(file_path)
    report["capa"] = run_capa(file_path)
    
    return report
