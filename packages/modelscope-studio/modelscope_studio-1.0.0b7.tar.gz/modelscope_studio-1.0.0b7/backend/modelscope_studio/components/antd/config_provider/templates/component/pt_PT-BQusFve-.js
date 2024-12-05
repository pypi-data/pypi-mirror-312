import { a as $ } from "./Index-Cq39SHXI.js";
import { i as l } from "./interopRequireDefault-BJV_i6Nz.js";
import { o as P, c as b } from "./common-DBXquc-F.js";
function x(u, v) {
  for (var p = 0; p < v.length; p++) {
    const a = v[p];
    if (typeof a != "string" && !Array.isArray(a)) {
      for (const r in a)
        if (r !== "default" && !(r in u)) {
          const m = Object.getOwnPropertyDescriptor(a, r);
          m && Object.defineProperty(u, r, m.get ? m : {
            enumerable: !0,
            get: () => a[r]
          });
        }
    }
  }
  return Object.freeze(Object.defineProperty(u, Symbol.toStringTag, {
    value: "Module"
  }));
}
var n = {}, i = {};
Object.defineProperty(i, "__esModule", {
  value: !0
});
i.default = void 0;
var S = {
  // Options
  items_per_page: "/ página",
  jump_to: "Saltar",
  jump_to_confirm: "confirmar",
  page: "Página",
  // Pagination
  prev_page: "Página Anterior",
  next_page: "Página Seguinte",
  prev_5: "Recuar 5 Páginas",
  next_5: "Avançar 5 Páginas",
  prev_3: "Recuar 3 Páginas",
  next_3: "Avançar 3 Páginas",
  page_size: "mărimea paginii"
};
i.default = S;
var c = {}, t = {}, d = {}, T = l.default;
Object.defineProperty(d, "__esModule", {
  value: !0
});
d.default = void 0;
var f = T(P), y = b, h = (0, f.default)((0, f.default)({}, y.commonLocale), {}, {
  locale: "pt_PT",
  today: "Hoje",
  now: "Agora",
  backToToday: "Hoje",
  ok: "OK",
  clear: "Limpar",
  month: "Mês",
  year: "Ano",
  timeSelect: "Selecionar hora",
  dateSelect: "Selecionar data",
  monthSelect: "Selecionar mês",
  yearSelect: "Selecionar ano",
  decadeSelect: "Selecionar década",
  dateFormat: "D/M/YYYY",
  dateTimeFormat: "D/M/YYYY HH:mm:ss",
  previousMonth: "Mês anterior (PageUp)",
  nextMonth: "Mês seguinte (PageDown)",
  previousYear: "Ano anterior (Control + left)",
  nextYear: "Ano seguinte (Control + right)",
  previousDecade: "Década anterior",
  nextDecade: "Década seguinte",
  previousCentury: "Século anterior",
  nextCentury: "Século seguinte",
  shortWeekDays: ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"],
  shortMonths: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
});
d.default = h;
var o = {};
Object.defineProperty(o, "__esModule", {
  value: !0
});
o.default = void 0;
const M = {
  placeholder: "Hora"
};
o.default = M;
var g = l.default;
Object.defineProperty(t, "__esModule", {
  value: !0
});
t.default = void 0;
var D = g(d), O = g(o);
const j = {
  lang: Object.assign(Object.assign({}, D.default), {
    placeholder: "Data",
    rangePlaceholder: ["Data inicial", "Data final"],
    today: "Hoje",
    now: "Agora",
    backToToday: "Hoje",
    ok: "OK",
    clear: "Limpar",
    month: "Mês",
    year: "Ano",
    timeSelect: "Hora",
    dateSelect: "Selecionar data",
    monthSelect: "Selecionar mês",
    yearSelect: "Selecionar ano",
    decadeSelect: "Selecionar década",
    yearFormat: "YYYY",
    dateFormat: "D/M/YYYY",
    dayFormat: "D",
    dateTimeFormat: "D/M/YYYY HH:mm:ss",
    monthFormat: "MMMM",
    monthBeforeYear: !1,
    previousMonth: "Mês anterior (PageUp)",
    nextMonth: "Mês seguinte (PageDown)",
    previousYear: "Ano anterior (Control + left)",
    nextYear: "Ano seguinte (Control + right)",
    previousDecade: "Última década",
    nextDecade: "Próxima década",
    previousCentury: "Último século",
    nextCentury: "Próximo século"
  }),
  timePickerLocale: Object.assign(Object.assign({}, O.default), {
    placeholder: "Hora"
  })
};
t.default = j;
var Y = l.default;
Object.defineProperty(c, "__esModule", {
  value: !0
});
c.default = void 0;
var A = Y(t);
c.default = A.default;
var s = l.default;
Object.defineProperty(n, "__esModule", {
  value: !0
});
n.default = void 0;
var C = s(i), F = s(c), k = s(t), R = s(o);
const e = "${label} não é um ${type} válido", q = {
  locale: "pt",
  Pagination: C.default,
  DatePicker: k.default,
  TimePicker: R.default,
  Calendar: F.default,
  global: {
    placeholder: "Por favor escolha"
  },
  Table: {
    filterTitle: "Filtro",
    filterConfirm: "Aplicar",
    filterReset: "Reiniciar",
    filterEmptyText: "Sem filtros",
    filterCheckall: "Selecionar todos os itens",
    filterSearchPlaceholder: "Pesquisar nos filtros",
    emptyText: "Sem conteúdo",
    selectAll: "Selecionar página atual",
    selectInvert: "Inverter seleção",
    sortTitle: "Ordenação",
    selectNone: "Apagar todo o conteúdo",
    selectionAll: "Selecionar todo o conteúdo",
    expand: "Expandir linha",
    collapse: "Colapsar linha",
    triggerDesc: "Clique organiza por descendente",
    triggerAsc: "Clique organiza por ascendente",
    cancelSort: "Clique para cancelar organização"
  },
  Modal: {
    okText: "OK",
    cancelText: "Cancelar",
    justOkText: "OK"
  },
  Popconfirm: {
    okText: "OK",
    cancelText: "Cancelar"
  },
  Transfer: {
    titles: ["", ""],
    searchPlaceholder: "Procurar...",
    itemUnit: "item",
    itemsUnit: "itens",
    remove: "Remover",
    selectCurrent: "Selecionar página atual",
    removeCurrent: "Remover página atual",
    selectAll: "Selecionar tudo",
    removeAll: "Remover tudo",
    selectInvert: "Inverter a página actual"
  },
  Upload: {
    uploading: "A carregar...",
    removeFile: "Remover",
    uploadError: "Erro ao carregar",
    previewFile: "Pré-visualizar",
    downloadFile: "Baixar"
  },
  Empty: {
    description: "Sem resultados"
  },
  Icon: {
    icon: "ícone"
  },
  Text: {
    edit: "editar",
    copy: "copiar",
    copied: "copiado",
    expand: "expandir"
  },
  Form: {
    optional: "(opcional)",
    defaultValidateMessages: {
      default: "Erro ${label} na validação de campo",
      required: "Por favor, insira ${label}",
      enum: "${label} deve ser um dos seguinte: [${enum}]",
      whitespace: "${label} não pode ser um carácter vazio",
      date: {
        format: " O formato de data ${label} é inválido",
        parse: "${label} não pode ser convertido para uma data",
        invalid: "${label} é uma data inválida"
      },
      types: {
        string: e,
        method: e,
        array: e,
        object: e,
        number: e,
        date: e,
        boolean: e,
        integer: e,
        float: e,
        regexp: e,
        email: e,
        url: e,
        hex: e
      },
      string: {
        len: "${label} deve possuir ${len} caracteres",
        min: "${label} deve possuir ao menos ${min} caracteres",
        max: "${label} deve possuir no máximo ${max} caracteres",
        range: "${label} deve possuir entre ${min} e ${max} caracteres"
      },
      number: {
        len: "${label} deve ser igual à ${len}",
        min: "O valor mínimo de ${label} é ${min}",
        max: "O valor máximo de ${label} é ${max}",
        range: "${label} deve estar entre ${min} e ${max}"
      },
      array: {
        len: "Deve ser ${len} ${label}",
        min: "No mínimo ${min} ${label}",
        max: "No máximo ${max} ${label}",
        range: "A quantidade de ${label} deve estar entre ${min} e ${max}"
      },
      pattern: {
        mismatch: "${label} não se enquadra no padrão ${pattern}"
      }
    }
  },
  Image: {
    preview: "Pré-visualização"
  }
};
n.default = q;
var _ = n;
const H = /* @__PURE__ */ $(_), I = /* @__PURE__ */ x({
  __proto__: null,
  default: H
}, [_]);
export {
  I as p
};
