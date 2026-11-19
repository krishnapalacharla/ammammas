"""Prepare supplied logo and a cohesive set of category window illustrations."""
from pathlib import Path
import xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];A=R/'theme/assets'
E.register_namespace('','http://www.w3.org/2000/svg')
ns={'s':'http://www.w3.org/2000/svg'}
logo=E.parse(R.parent/'horizontal logo.svg').getroot()
typegroup=logo.find('s:g/s:g',ns)[1]
# Remove the two bottom language labels, retain the supplied outlined wordmark.
for group in list(typegroup):
    if any(float(t.attrib.get('transform','translate(0 0)').split()[-1].rstrip(')'))>180 for t in group.findall('s:text',ns)):
        typegroup.remove(group)
typegroup.set('transform','translate(0 28)')
# The small descriptor is live text in Illustrator; use a portable, legible line.
descriptor=typegroup.findall('s:g',ns)[1]
for c in list(descriptor):descriptor.remove(c)
text=E.SubElement(descriptor,'{'+ns['s']+'}text',{'x':'553','y':'154','text-anchor':'middle','style':'font:600 23px Arial,sans-serif;letter-spacing:1px;fill:#77290d'})
text.text='SPICES  |  GHEE  |  PICKLES  |  SNACKS'
for p in [A/'ammammas-logo.svg',R/'brand-assets/logos/ammammas-logo.svg']:
    E.ElementTree(logo).write(p,encoding='unicode')
# Footer keeps the two language labels from the supplied original artwork.
footer=E.parse(R.parent/'horizontal logo.svg').getroot()
for text in footer.findall('.//s:text',ns):
    if '208' in text.attrib.get('transform',''):
        text.set('style','font:600 20px Arial,sans-serif;fill:#77290d')
footer_type=footer.find('s:g/s:g',ns)[1]
footer_type.set('transform','translate(0 7)')
footer_descriptor=footer_type.findall('s:g',ns)[1]
for child in list(footer_descriptor):footer_descriptor.remove(child)
footer_text=E.SubElement(footer_descriptor,'{'+ns['s']+'}text',{'x':'553','y':'154','text-anchor':'middle','style':'font:600 23px Arial,sans-serif;letter-spacing:1px;fill:#77290d'})
footer_text.text='SPICES  |  GHEE  |  PICKLES  |  SNACKS'
E.ElementTree(footer).write(A/'ammammas-footer-logo.svg',encoding='unicode')
art={
'pickles':('<path fill="#fdbb5b" d="M58 61H122V131Q90 148 58 131Z"/>','<path d="M57 59H123V132Q90 148 57 132ZM53 49H127V60H53ZM62 42H118V49M66 81Q91 66 114 84M69 122Q91 136 111 119"/><path d="M78 89Q96 78 109 93Q94 118 77 110Q67 102 78 89ZM89 98L104 90M73 34Q81 19 95 23Q98 34 84 38M90 37L96 26"/>'),
'spices':('<path fill="#fdbb5b" d="M39 104H141L128 135H52Z"/>','<path d="M38 104H142L128 136H52ZM48 103L69 79L82 85L101 67L132 104M100 67L111 46M107 49L121 28Q126 22 132 29L136 34Q139 38 134 44L117 60M57 48L64 57M49 65L58 68M77 42V52M78 95L81 95M105 91H108M62 112Q90 126 119 112"/>'),
'ready-to-cook':('<ellipse fill="#fdbb5b" cx="90" cy="113" rx="59" ry="22"/>','<ellipse cx="90" cy="119" rx="62" ry="23"/><ellipse cx="90" cy="109" rx="54" ry="19"/><path d="M47 103Q53 76 82 82L130 103Q111 124 47 103ZM82 82Q96 75 130 103M56 111Q88 128 123 111M63 65Q53 54 64 43M88 62Q78 47 91 34M113 67Q102 56 115 44M67 98H70M83 104H86M103 106H106"/>'),
'ghee':('<path fill="#fdbb5b" d="M59 76Q40 101 57 132H123Q140 101 121 76Z"/>','<path d="M65 64H115V76Q137 91 125 131Q92 147 55 131Q43 94 65 76ZM61 54H119V65H61ZM72 47H108V54M68 94Q91 107 113 94M75 113Q89 125 105 113M132 39L121 66M134 34L147 28Q154 31 150 38L137 44ZM90 76Q75 91 90 96Q104 91 90 76Z"/>'),
'snacks':('<path fill="#fdbb5b" d="M37 109H143L129 136H51Z"/>','<path d="M36 109H144L129 136H51ZM52 103Q29 84 52 66Q80 50 96 77Q108 101 82 105Q61 104 64 84Q67 72 78 81Q86 91 75 92M96 102Q112 66 132 89Q142 106 124 107M103 59Q101 40 119 43Q133 49 121 61Q109 70 103 59ZM59 120Q90 130 120 120"/>'),
'fryum-factory':('<ellipse fill="#fdbb5b" cx="90" cy="124" rx="61" ry="20"/>','<ellipse cx="90" cy="126" rx="62" ry="21"/><path d="M42 119L63 83L83 119ZM51 113H73M59 100H66M99 111L107 75L126 80L118 117ZM107 87L119 90M105 98L116 101M105 47L111 54M86 53L83 60"/><circle cx="83" cy="92" r="14"/><circle cx="83" cy="92" r="6"/><path d="M70 133Q91 140 113 131"/>'),
'retro':('<path fill="#fdbb5b" d="M56 66H124V132Q90 147 56 132Z"/>','<path d="M56 66H124V132Q90 147 56 132ZM51 53H129V66H51ZM72 46H108V53M65 83H115V119H65Z"/><circle cx="81" cy="97" r="7"/><path d="M96 91L105 103M100 89L109 101M76 112H101M39 74L29 64M35 87H24M139 74L148 65M143 88H154"/>'),
}
for name,(fill,lines) in art.items():
    (A/('category-'+name+'.svg')).write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 180"><g opacity=".48">'+fill+'</g><g fill="none" stroke="#77290d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'+lines+'</g></svg>',encoding='utf-8')
# The original tree crown extends beyond y=0; padding must live inside its viewBox.
p=A/'village-street.svg';s=p.read_text(encoding='utf-8');s=s.replace('viewBox="0 0 1440 310"','viewBox="-12 -48 1464 370"');p.write_text(s,encoding='utf-8')
print('Simplified logo, seven category illustrations and uncropped village prepared.')
