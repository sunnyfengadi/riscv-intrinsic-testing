# The map of all api type for templates
TEMPLATE_TYPE={
    'CSR Register Configure: CSR Read':                'template_head.c',
    'CSR Register Configure: CSR Scalar Write':        'template_head.c',
    'CSR Register Configure: CSR immediate Write':     'template_head.c',
    'Contiguous Load: Unmasked Load':                  ['common_tail_1.c', 'common_tail_x.c'],
    'Contiguous Load: Masked Load':                    ['common_tail_1.c', 'common_tail_x.c'],
    'Contiguous Store: Unmasked Store':                ['store_tail_1.c', 'store_tail_x.c'],
    'Contiguous Store: Masked Store':                  ['store_tail_1.c', 'store_tail_x.c'],
    'Interleave Load: Unmasked Load':                  ['common_tail_1.c', 'common_tail_x.c'],
    'Interleave Load: Masked Load':                    ['common_tail_1.c', 'common_tail_x.c'],
    'Interleave Store: Unmasked Store':                ['store_tail_1.c', 'store_tail_x.c'],
    'Interleave Store: Masked Store':                  ['store_tail_1.c', 'store_tail_x.c'],
    'Indexed Load: Unmasked Load':                     ['common_tail_1.c', 'common_tail_x.c'],
    'Indexed Load: Masked Load':                       ['common_tail_1.c', 'common_tail_x.c'],
    'Indexed Store: Unmasked Store':                   ['store_tail_1.c', 'store_tail_x.c'],
    'Indexed Store: Masked Store':                     ['store_tail_1.c', 'store_tail_x.c'],
    'Arithmetic: Unmasked Add':                        ['common_tail_1.c', 'common_tail_x.c'],
    'Arithmetic: Masked Add':                          ['common_tail_1.c', 'common_tail_x.c'],
    'Arithmetic: Unmasked Sub':                        ['common_tail_1.c', 'common_tail_x.c'],
    'Arithmetic: Masked Sub':                          ['common_tail_1.c', 'common_tail_x.c'],
    'Arithmetic: Unmasked Multiply':                   ['common_tail_1.c', 'common_tail_x.c'],
    'Arithmetic: Masked Multiply':                     ['common_tail_1.c', 'common_tail_x.c'],
    'Arithmetic: Unmasked Neg':                        ['common_tail_1.c', 'common_tail_x.c'],
    'Arithmetic: Masked Neg':                          ['common_tail_1.c', 'common_tail_x.c'],
    'Arithmetic: Unmasked Min':                        ['common_tail_1.c', 'common_tail_x.c'],
    'Arithmetic: Masked Min':                          ['common_tail_1.c', 'common_tail_x.c'],
    'Arithmetic: Unmasked Max':                        ['common_tail_1.c', 'common_tail_x.c'],
    'Arithmetic: Masked Max':                          ['common_tail_1.c', 'common_tail_x.c'],
    'Logic: Unmasked Vector logical':                  ['common_tail_1.c', 'common_tail_x.c'],
    'Logic: Masked Vector logical':                    ['common_tail_1.c', 'common_tail_x.c'],
    'Logic: Unmasked Mask logical':                    ['common_tail_1.c', 'common_tail_x.c'],
    'Logic: Masked Mask logical':                      ['common_tail_1.c', 'common_tail_x.c'],
    'Shift: Unmasked Logic Shift Left':                ['common_tail_1.c', 'common_tail_x.c'],
    'Shift: Masked Logic Shift Left':                  ['common_tail_1.c', 'common_tail_x.c'],
    'Shift: Unmasked Logic Shift Right':               ['common_tail_1.c', 'common_tail_x.c'],
    'Shift: Masked Logic Shift Right':                 ['common_tail_1.c', 'common_tail_x.c'],
    'Shift: Unmasked Arithmetic Shift Right':          ['common_tail_1.c', 'common_tail_x.c'],
    'Shift: Masked Arithmetic Shift Right':            ['common_tail_1.c', 'common_tail_x.c'],
    'Shift: Unmasked Accumulator Shift Right':         ['common_tail_1.c', 'common_tail_x.c'],
    'Shift: Masked Accumulator Shift Right':           ['common_tail_1.c', 'common_tail_x.c'],
    'Shift: Unmasked Circular Buffer Shift Left':      ['common_tail_1.c', 'common_tail_x.c'],
    'Shift: Masked Circular Buffer Shift Left':        ['common_tail_1.c', 'common_tail_x.c'],
    'Shift: Unmasked Circular Buffer Shift Right':     ['common_tail_1.c', 'common_tail_x.c'],
    'Shift: Masked Circular Buffer Shift Right':       ['common_tail_1.c', 'common_tail_x.c'],
    'Shift: Mask Shift Left':                          ['common_tail_1.c', 'common_tail_x.c'],
    'Mac: Unmasked Multiply-Add':                      'template_head.c',
    'Mac: Masked Multiply-Add':                        'template_head.c',
    'Mac: Unmasked Multiply-Subtract':                 'template_head.c',
    'Mac: Masked Multiply-Subtract':                   'template_head.c',
    'Mac: Unmasked Multiply-Neg-Add':                  'template_head.c',
    'Mac: Masked Multiply-Neg-Add':                    'template_head.c',
    'Mac: Unmasked Multiply-Neg-Subtract':             'template_head.c',
    'Mac: Masked Multiply-Neg-Subtract':               'template_head.c',
    'Reduction: Unmasked Reduce Sum':                  'template_head.c',
    'Reduction: Masked Reduce Sum':                    'template_head.c',
    'Reduction: Unmasked Reduce Dot':                  'template_head.c',
    'Reduction: Masked Reduce Dot':                    'template_head.c',
    'Reduction: Unmasked Reduce Min':                  'template_head.c',
    'Reduction: Masked Reduce Min':                    'template_head.c',
    'Reduction: Unmasked Reduce Max':                  'template_head.c',
    'Reduction: Masked Reduce Min':                    'template_head.c',
    'Move: Unmasked Duplicate':                        'template_head.c',
    'Move: Masked Duplicate':                          'template_head.c',
    'Move: Unmasked Extract':                          'template_head.c',
    'Move: Masked Extract':                            'template_head.c',
    'Move: Masket Intrinsic':                          'template_head.c',
    'Permutation: Unmasked Gather Intrinsic':          'template_head.c',
    'Permutation: Masked Gather Intrinsic':            'template_head.c',
    'Permutation: Merge Intrinsic':                    'template_head.c',
    'Conversion: Unmasked Extend Intrinsic':           'template_head.c',
    'Conversion: Masked Extend Intrinsic':             'template_head.c',
    'Conversion: Unmasked Truncate Intrinsic':         'template_head.c',
    'Conversion: Masked Truncate Intrinsic':           'template_head.c',
    'Conversion: Unmasked Clip Intrinsic':             'template_head.c',
    'Conversion: Masked Clip Intrinsic':               'template_head.c',
    'Compare: Unmasked EQ Intrinsic':                  'template_head.c',
    'Compare: Masked EQ Intrinsic':                    'template_head.c',
    'Compare: Unmasked NE Intrinsic':                  'template_head.c',
    'Compare: masked NE Intrinsic':                    'template_head.c',
    'Compare: Unmasked LT Intrinsic':                  'template_head.c',
    'Compare: Masked LT Intrinsic':                    'template_head.c',
    'Compare: Unmasked LE Intrinsic':                  'template_head.c',
    'Compare: Masked LE Intrinsic':                    'template_head.c',
    'Compare: Unmasked GT Intrinsic':                  'template_head.c',
    'Compare: Masked GT Intrinsic':                    'template_head.c',
    'Compare: Unmasked GE Intrinsic':                  'template_head.c',
    'Compare: Masked GE Intrinsic':                    'template_head.c',
    'IIR: Signed Fract Clear Dotiir':                  'template_head.c',
    'IIR: Signed Fract Dotiir':                        'template_head.c',
    'IIR: Unsigned Fract Clear Dotiir':                'template_head.c',
    'IIR: Unsigned Fract Dotiir':                      'template_head.c',
}