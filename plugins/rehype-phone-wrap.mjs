import { visit } from 'unist-util-visit';

const PHONE_PATTERN = /\(801\)\s*814-6975/g;

export function rehypePhoneWrap() {
  return (tree) => {
    visit(tree, 'text', (node, index, parent) => {
      if (!parent || typeof index !== 'number') return;
      if (parent.type === 'element' && parent.tagName === 'a' && parent.properties?.href?.toString().startsWith('tel:')) {
        parent.properties['data-ghl-phone'] = '';
        return;
      }
      if (!PHONE_PATTERN.test(node.value)) return;
      PHONE_PATTERN.lastIndex = 0;

      const parts = [];
      let lastIndex = 0;
      let match;
      while ((match = PHONE_PATTERN.exec(node.value)) !== null) {
        if (match.index > lastIndex) {
          parts.push({ type: 'text', value: node.value.slice(lastIndex, match.index) });
        }
        parts.push({
          type: 'element',
          tagName: 'span',
          properties: { 'data-ghl-phone': '' },
          children: [{ type: 'text', value: match[0] }],
        });
        lastIndex = match.index + match[0].length;
      }
      if (lastIndex < node.value.length) {
        parts.push({ type: 'text', value: node.value.slice(lastIndex) });
      }
      parent.children.splice(index, 1, ...parts);
      return index + parts.length;
    });
  };
}
