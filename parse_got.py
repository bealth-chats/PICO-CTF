import sys
from elftools.elf.elffile import ELFFile

with open("beacon", "rb") as f:
    elf = ELFFile(f)
    print("Entry point:", hex(elf.header['e_entry']))

    for section in elf.iter_sections():
        print(f"Section {section.name} at {hex(section.header['sh_addr'])} size {hex(section.header['sh_size'])}")

    rela_dyn = elf.get_section_by_name('.rela.dyn')
    if rela_dyn:
        print("Relocations:")
        for reloc in rela_dyn.iter_relocations():
            print(f"  Offset: {hex(reloc['r_offset'])}, Type: {reloc['r_info_type']}, Addend: {hex(reloc['r_addend'])}")
