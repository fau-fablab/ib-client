gl.setup(1024, 768)

font_silk = resource.load_font("silkscreen.ttf")
font_h = resource.load_font("Roboto-Black.ttf")

-- Betreuer
image_man = resource.load_image("woman.png")
image_woman = resource.load_image("man.png")

img_list_bg = resource.load_image("list-bg-1.png")

function node.render()
    font_silk:write(12, 620, "Hello World, this is FabLab", 32, 1, 1, 1, 1)

    -- Termine
    font_h:write(10, 10, "Termine", 56, 1, 1, 1, 1)

    w_li,h_li = img_list_bg:size()
    local x = 10
    local y = 100
    local w = w_li / 2
    local h = h_li / 2
    img_list_bg:draw(x, y, x + w, y + h)



    -- Betreuer
    x = WIDTH / 2 - 50
    width_man,height_man = image_man:size()
    width_woman,height_woman = image_woman:size()
    y = 100
    w = width_man

    font_h:write(x, 10, "Betreuer", 56, 1, 1, 1, 1)
    h = height_man

    image_man:draw(x, y, x + width_man, y + height_man)

    x = x + width_man + 10
    w = width_woman
    h = height_woman
    image_woman:draw(x, y, x + width_man, y + height_man)
end
