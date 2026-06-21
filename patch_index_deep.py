import sys

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_html = """                        <div class="crit-feedback">
                           <div class="crit-feedback-label">RETROALIMENTACIÓN IA:</div>
                           <div class="crit-feedback-text" x-text="crit.feedback"></div>
                        </div>"""

new_html = """                        <div class="crit-feedback">
                           <div class="crit-feedback-label">RETROALIMENTACIÓN IA:</div>
                           
                           <template x-if="typeof crit.feedback === 'object' && crit.feedback !== null">
                              <div>
                                 <div class="crit-feedback-text" x-text="crit.feedback.justification" style="margin-bottom: 12px;"></div>
                                 
                                 <template x-if="crit.feedback.errors && crit.feedback.errors.length > 0">
                                    <div style="margin-bottom: 12px; background: rgba(248, 113, 113, 0.05); padding: 12px; border-radius: 8px; border-left: 2px solid #f87171;">
                                       <div style="color: #fca5a5; font-size: 11px; font-weight: 700; margin-bottom: 6px; letter-spacing: 0.5px;">❌ ERRORES / FALLAS IDENTIFICADAS:</div>
                                       <ul style="margin: 0; padding-left: 16px; color: #cbd5e1; font-size: 13px; line-height: 1.5;">
                                          <template x-for="err in crit.feedback.errors">
                                             <li x-text="err" style="margin-bottom: 4px;"></li>
                                          </template>
                                       </ul>
                                    </div>
                                 </template>

                                 <template x-if="crit.feedback.strengths && crit.feedback.strengths.length > 0">
                                    <div style="background: rgba(74, 222, 128, 0.05); padding: 12px; border-radius: 8px; border-left: 2px solid #4ade80;">
                                       <div style="color: #86efac; font-size: 11px; font-weight: 700; margin-bottom: 6px; letter-spacing: 0.5px;">✅ FORTALEZAS DESTACADAS:</div>
                                       <ul style="margin: 0; padding-left: 16px; color: #cbd5e1; font-size: 13px; line-height: 1.5;">
                                          <template x-for="str in crit.feedback.strengths">
                                             <li x-text="str" style="margin-bottom: 4px;"></li>
                                          </template>
                                       </ul>
                                    </div>
                                 </template>
                              </div>
                           </template>

                           <template x-if="typeof crit.feedback === 'string'">
                              <div class="crit-feedback-text" x-text="crit.feedback"></div>
                           </template>

                        </div>"""

if old_html in content:
    content = content.replace(old_html, new_html)
else:
    print("WARNING: Could not find old HTML block. Trying partial...", flush=True)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
