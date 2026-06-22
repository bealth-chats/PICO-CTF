# Where does `1300` return its seed?!
# `1351: cmove eax, ecx`
# `1354: pop rcx`
# `1355: ret`
# SO I SHOULD PATCH `134c`!
# `134c` is `b9 01 00 00 00` (mov ecx, 1)
# `1351` is `0f 44 c1` (cmove eax, ecx)
# `1354` is `59` (pop rcx)
# `1355` is `c3` (ret)
# I can patch `1349` with `mov eax, seed` (`b8 XX XX 00 00`)!
# Then `134e: nop; nop; nop` (`90 90 90`)
# Let's check the EXACT offset and bytes!
