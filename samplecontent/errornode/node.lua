gl.setup(1024, 768)

-- font_silk = resource.load_font("silkscreen.ttf")
local font = resource.load_font("Roboto-Regular.ttf")
local lines = {}
local image_logo = resource.load_image("fablab_logo.png")
local width, height = image_logo:size()

local white = resource.create_colored_texture(1,1,1,1)


function wrap(str, limit, indent, indent1)
    indent = indent or ""
    indent1 = indent1 or indent
    function wrap_parargraph(str)
        local here = 1-#indent1
        return indent1..str:gsub("(%s+)()(%S+)()", function(sp, st, word, fi)
            if fi-here > limit then
                here = st - #indent
                return "\n"..indent..word
            end
        end)
    end
    local splitted = {}
    for par in string.gmatch(str, "[^\n]+") do
        local wrapped = wrap_parargraph(par)
        for line in string.gmatch(wrapped, "[^\n]+") do
            splitted[#splitted + 1] = line
        end
    end
    return splitted
end

util.file_watch("error.txt", function(content)
    lines = wrap(content, 100)
end)



function node.render()
    gl.clear(0, 0, 0, 0)

   -- font_silk:write(12, 320, "Hello World, this is FabLab", 32, 1, 1, 1, 1)

   -- font_silk:write(10, 10, "Termine", 64, 1, 1, 1, 1)

    local w = 2*width
    local h = 2*height
    local x = (WIDTH - w)/2
    local y = 100
    white:draw(x, y, x+w, y+h)
    image_logo:draw(x, y, x+w, y+h)

    x = 10
    y = y + h + 150

--    font:write(x, y, "TEXT", 32, 1, 1, 1, 0.8)
    for i, line in ipairs(lines) do
        local size = 24
        font:write(x, y, line, size, 1, 1, 1, 1)
        y = y + size
    end

end
