-- Give markdown pipe tables wrapping columns.
-- Header text is matched so wide "Basis" / "Change" cells stay inside the measure.
-- Widths are fractions of the text line and must sum to 1.

local PRESETS = {
  ["3|#"] = {0.07, 0.14, 0.79},
  ["4|Animal"] = {0.24, 0.22, 0.18, 0.36},
  ["4|Cluster"] = {0.22, 0.13, 0.15, 0.50},
  ["5|Group"] = {0.34, 0.24, 0.08, 0.18, 0.16},
  ["5|Dropped animal"] = {0.26, 0.10, 0.24, 0.18, 0.22},
  ["5|Statistic"] = {0.30, 0.18, 0.16, 0.20, 0.16},
  ["5|Scheme"] = {0.30, 0.26, 0.08, 0.20, 0.16},
}

local function header_key(tbl)
  local ncols = #tbl.colspecs
  local first = ""
  if tbl.head and tbl.head.rows and #tbl.head.rows > 0 then
    local cell = tbl.head.rows[1].cells[1]
    if cell then
      first = pandoc.utils.stringify(cell.contents or cell)
    end
  end
  return ncols .. "|" .. first, ncols
end

function Table(tbl)
  local key, ncols = header_key(tbl)
  if ncols == 0 then
    return tbl
  end
  local widths = PRESETS[key]
  if not widths then
    io.stderr:write("pdf_table_widths: no preset for '" .. key .. "'; using equal widths\n")
    widths = {}
    for i = 1, ncols do
      widths[i] = 1.0 / ncols
    end
  end
  if #widths ~= ncols then
    io.stderr:write("pdf_table_widths: preset length mismatch for '" .. key .. "'\n")
    return tbl
  end
  for i = 1, ncols do
    tbl.colspecs[i] = {pandoc.AlignLeft, widths[i]}
  end
  return tbl
end
