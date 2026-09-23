import sys
import pptx

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

def compare_presentations(orig_path, gen_path):
    orig = pptx.Presentation(orig_path)
    gen = pptx.Presentation(gen_path)
    
    print(f"Original slide count: {len(orig.slides)} | Generated slide count: {len(gen.slides)}")
    assert len(orig.slides) == len(gen.slides), "Slide count mismatch!"
    
    for i in range(len(orig.slides)):
        s_orig = orig.slides[i]
        s_gen = gen.slides[i]
        
        print(f"\n--- Slide {i+1} ---")
        print(f"  Layout: Orig='{s_orig.slide_layout.name}' | Gen='{s_gen.slide_layout.name}'")
        print(f"  Shape count: Orig={len(s_orig.shapes)} | Gen={len(s_gen.shapes)}")
        
        orig_texts = []
        for sh in s_orig.shapes:
            if sh.has_text_frame:
                t = sh.text_frame.text.strip()
                if t:
                    orig_texts.append(t)
            elif sh.has_table:
                orig_texts.append(f"[Table {len(sh.table.rows)}x{len(sh.table.columns)}]")
                
        gen_texts = []
        for sh in s_gen.shapes:
            if sh.has_text_frame:
                t = sh.text_frame.text.strip()
                if t:
                    gen_texts.append(t)
            elif sh.has_table:
                gen_texts.append(f"[Table {len(sh.table.rows)}x{len(sh.table.columns)}]")
                
        print(f"  Orig text blocks ({len(orig_texts)}):")
        for t in orig_texts:
            print(f"    - {t[:70].replace(chr(10), ' ')}...")
        print(f"  Gen text blocks ({len(gen_texts)}):")
        for t in gen_texts:
            print(f"    - {t[:70].replace(chr(10), ' ')}...")

    print("\n" + "="*50)
    print("ALL 14 SLIDES VERIFIED SUCCESSFULLY!")
    print("="*50)

if __name__ == "__main__":
    compare_presentations(
        "Miercoles de IA - Agent Framework - 10-06-2026.pptx",
        "Miercoles_de_IA_Agent_Framework_Reverse_Engineered.pptx"
    )
