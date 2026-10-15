"""Regenerates sections 5 to 9 with lower_sections.py and splices them into src/home-content.html. Run from the homepage folder."""
import pathlib, subprocess, sys
gen = subprocess.run([sys.executable, '-I', 'tools/lower_sections.py'], capture_output=True, text=True, check=True).stdout
p = pathlib.Path('src/home-content.html'); t = p.read_text()
a = t.index('  <!-- ========== 5. Store finder ========== -->'); b = t.index('  <!-- ========== 10. FAQ ========== -->')
p.write_text(t[:a] + gen + '\n' + t[b:])
print('sections 5 to 9 regenerated')
