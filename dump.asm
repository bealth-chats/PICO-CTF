
system.out:     file format elf64-x86-64


Disassembly of section .init:

0000000000001000 <_init>:
    1000:	f3 0f 1e fa          	endbr64
    1004:	48 83 ec 08          	sub    rsp,0x8
    1008:	48 8b 05 d9 2f 00 00 	mov    rax,QWORD PTR [rip+0x2fd9]        # 3fe8 <__gmon_start__@Base>
    100f:	48 85 c0             	test   rax,rax
    1012:	74 02                	je     1016 <_init+0x16>
    1014:	ff d0                	call   rax
    1016:	48 83 c4 08          	add    rsp,0x8
    101a:	c3                   	ret

Disassembly of section .plt:

0000000000001020 <.plt>:
    1020:	ff 35 2a 2f 00 00    	push   QWORD PTR [rip+0x2f2a]        # 3f50 <_GLOBAL_OFFSET_TABLE_+0x8>
    1026:	ff 25 2c 2f 00 00    	jmp    QWORD PTR [rip+0x2f2c]        # 3f58 <_GLOBAL_OFFSET_TABLE_+0x10>
    102c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
    1030:	f3 0f 1e fa          	endbr64
    1034:	68 00 00 00 00       	push   0x0
    1039:	e9 e2 ff ff ff       	jmp    1020 <_init+0x20>
    103e:	66 90                	xchg   ax,ax
    1040:	f3 0f 1e fa          	endbr64
    1044:	68 01 00 00 00       	push   0x1
    1049:	e9 d2 ff ff ff       	jmp    1020 <_init+0x20>
    104e:	66 90                	xchg   ax,ax
    1050:	f3 0f 1e fa          	endbr64
    1054:	68 02 00 00 00       	push   0x2
    1059:	e9 c2 ff ff ff       	jmp    1020 <_init+0x20>
    105e:	66 90                	xchg   ax,ax
    1060:	f3 0f 1e fa          	endbr64
    1064:	68 03 00 00 00       	push   0x3
    1069:	e9 b2 ff ff ff       	jmp    1020 <_init+0x20>
    106e:	66 90                	xchg   ax,ax
    1070:	f3 0f 1e fa          	endbr64
    1074:	68 04 00 00 00       	push   0x4
    1079:	e9 a2 ff ff ff       	jmp    1020 <_init+0x20>
    107e:	66 90                	xchg   ax,ax
    1080:	f3 0f 1e fa          	endbr64
    1084:	68 05 00 00 00       	push   0x5
    1089:	e9 92 ff ff ff       	jmp    1020 <_init+0x20>
    108e:	66 90                	xchg   ax,ax
    1090:	f3 0f 1e fa          	endbr64
    1094:	68 06 00 00 00       	push   0x6
    1099:	e9 82 ff ff ff       	jmp    1020 <_init+0x20>
    109e:	66 90                	xchg   ax,ax
    10a0:	f3 0f 1e fa          	endbr64
    10a4:	68 07 00 00 00       	push   0x7
    10a9:	e9 72 ff ff ff       	jmp    1020 <_init+0x20>
    10ae:	66 90                	xchg   ax,ax
    10b0:	f3 0f 1e fa          	endbr64
    10b4:	68 08 00 00 00       	push   0x8
    10b9:	e9 62 ff ff ff       	jmp    1020 <_init+0x20>
    10be:	66 90                	xchg   ax,ax
    10c0:	f3 0f 1e fa          	endbr64
    10c4:	68 09 00 00 00       	push   0x9
    10c9:	e9 52 ff ff ff       	jmp    1020 <_init+0x20>
    10ce:	66 90                	xchg   ax,ax
    10d0:	f3 0f 1e fa          	endbr64
    10d4:	68 0a 00 00 00       	push   0xa
    10d9:	e9 42 ff ff ff       	jmp    1020 <_init+0x20>
    10de:	66 90                	xchg   ax,ax
    10e0:	f3 0f 1e fa          	endbr64
    10e4:	68 0b 00 00 00       	push   0xb
    10e9:	e9 32 ff ff ff       	jmp    1020 <_init+0x20>
    10ee:	66 90                	xchg   ax,ax
    10f0:	f3 0f 1e fa          	endbr64
    10f4:	68 0c 00 00 00       	push   0xc
    10f9:	e9 22 ff ff ff       	jmp    1020 <_init+0x20>
    10fe:	66 90                	xchg   ax,ax
    1100:	f3 0f 1e fa          	endbr64
    1104:	68 0d 00 00 00       	push   0xd
    1109:	e9 12 ff ff ff       	jmp    1020 <_init+0x20>
    110e:	66 90                	xchg   ax,ax
    1110:	f3 0f 1e fa          	endbr64
    1114:	68 0e 00 00 00       	push   0xe
    1119:	e9 02 ff ff ff       	jmp    1020 <_init+0x20>
    111e:	66 90                	xchg   ax,ax

Disassembly of section .plt.got:

0000000000001120 <__cxa_finalize@plt>:
    1120:	f3 0f 1e fa          	endbr64
    1124:	ff 25 ce 2e 00 00    	jmp    QWORD PTR [rip+0x2ece]        # 3ff8 <__cxa_finalize@GLIBC_2.2.5>
    112a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

Disassembly of section .plt.sec:

0000000000001130 <free@plt>:
    1130:	f3 0f 1e fa          	endbr64
    1134:	ff 25 26 2e 00 00    	jmp    QWORD PTR [rip+0x2e26]        # 3f60 <free@GLIBC_2.2.5>
    113a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001140 <putchar@plt>:
    1140:	f3 0f 1e fa          	endbr64
    1144:	ff 25 1e 2e 00 00    	jmp    QWORD PTR [rip+0x2e1e]        # 3f68 <putchar@GLIBC_2.2.5>
    114a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001150 <strcpy@plt>:
    1150:	f3 0f 1e fa          	endbr64
    1154:	ff 25 16 2e 00 00    	jmp    QWORD PTR [rip+0x2e16]        # 3f70 <strcpy@GLIBC_2.2.5>
    115a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001160 <puts@plt>:
    1160:	f3 0f 1e fa          	endbr64
    1164:	ff 25 0e 2e 00 00    	jmp    QWORD PTR [rip+0x2e0e]        # 3f78 <puts@GLIBC_2.2.5>
    116a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001170 <fclose@plt>:
    1170:	f3 0f 1e fa          	endbr64
    1174:	ff 25 06 2e 00 00    	jmp    QWORD PTR [rip+0x2e06]        # 3f80 <fclose@GLIBC_2.2.5>
    117a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001180 <strlen@plt>:
    1180:	f3 0f 1e fa          	endbr64
    1184:	ff 25 fe 2d 00 00    	jmp    QWORD PTR [rip+0x2dfe]        # 3f88 <strlen@GLIBC_2.2.5>
    118a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001190 <__stack_chk_fail@plt>:
    1190:	f3 0f 1e fa          	endbr64
    1194:	ff 25 f6 2d 00 00    	jmp    QWORD PTR [rip+0x2df6]        # 3f90 <__stack_chk_fail@GLIBC_2.4>
    119a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000011a0 <printf@plt>:
    11a0:	f3 0f 1e fa          	endbr64
    11a4:	ff 25 ee 2d 00 00    	jmp    QWORD PTR [rip+0x2dee]        # 3f98 <printf@GLIBC_2.2.5>
    11aa:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000011b0 <__assert_fail@plt>:
    11b0:	f3 0f 1e fa          	endbr64
    11b4:	ff 25 e6 2d 00 00    	jmp    QWORD PTR [rip+0x2de6]        # 3fa0 <__assert_fail@GLIBC_2.2.5>
    11ba:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000011c0 <fgets@plt>:
    11c0:	f3 0f 1e fa          	endbr64
    11c4:	ff 25 de 2d 00 00    	jmp    QWORD PTR [rip+0x2dde]        # 3fa8 <fgets@GLIBC_2.2.5>
    11ca:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000011d0 <calloc@plt>:
    11d0:	f3 0f 1e fa          	endbr64
    11d4:	ff 25 d6 2d 00 00    	jmp    QWORD PTR [rip+0x2dd6]        # 3fb0 <calloc@GLIBC_2.2.5>
    11da:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000011e0 <fopen@plt>:
    11e0:	f3 0f 1e fa          	endbr64
    11e4:	ff 25 ce 2d 00 00    	jmp    QWORD PTR [rip+0x2dce]        # 3fb8 <fopen@GLIBC_2.2.5>
    11ea:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000000000011f0 <perror@plt>:
    11f0:	f3 0f 1e fa          	endbr64
    11f4:	ff 25 c6 2d 00 00    	jmp    QWORD PTR [rip+0x2dc6]        # 3fc0 <perror@GLIBC_2.2.5>
    11fa:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001200 <strtoul@plt>:
    1200:	f3 0f 1e fa          	endbr64
    1204:	ff 25 be 2d 00 00    	jmp    QWORD PTR [rip+0x2dbe]        # 3fc8 <strtoul@GLIBC_2.2.5>
    120a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000001210 <atoi@plt>:
    1210:	f3 0f 1e fa          	endbr64
    1214:	ff 25 b6 2d 00 00    	jmp    QWORD PTR [rip+0x2db6]        # 3fd0 <atoi@GLIBC_2.2.5>
    121a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

Disassembly of section .text:

0000000000001220 <_start>:
    1220:	f3 0f 1e fa          	endbr64
    1224:	31 ed                	xor    ebp,ebp
    1226:	49 89 d1             	mov    r9,rdx
    1229:	5e                   	pop    rsi
    122a:	48 89 e2             	mov    rdx,rsp
    122d:	48 83 e4 f0          	and    rsp,0xfffffffffffffff0
    1231:	50                   	push   rax
    1232:	54                   	push   rsp
    1233:	45 31 c0             	xor    r8d,r8d
    1236:	31 c9                	xor    ecx,ecx
    1238:	48 8d 3d 91 01 00 00 	lea    rdi,[rip+0x191]        # 13d0 <main>
    123f:	ff 15 93 2d 00 00    	call   QWORD PTR [rip+0x2d93]        # 3fd8 <__libc_start_main@GLIBC_2.34>
    1245:	f4                   	hlt
    1246:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    124d:	00 00 00

0000000000001250 <deregister_tm_clones>:
    1250:	48 8d 3d b9 2d 00 00 	lea    rdi,[rip+0x2db9]        # 4010 <stdin@GLIBC_2.2.5>
    1257:	48 8d 05 b2 2d 00 00 	lea    rax,[rip+0x2db2]        # 4010 <stdin@GLIBC_2.2.5>
    125e:	48 39 f8             	cmp    rax,rdi
    1261:	74 15                	je     1278 <deregister_tm_clones+0x28>
    1263:	48 8b 05 76 2d 00 00 	mov    rax,QWORD PTR [rip+0x2d76]        # 3fe0 <_ITM_deregisterTMCloneTable@Base>
    126a:	48 85 c0             	test   rax,rax
    126d:	74 09                	je     1278 <deregister_tm_clones+0x28>
    126f:	ff e0                	jmp    rax
    1271:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    1278:	c3                   	ret
    1279:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

0000000000001280 <register_tm_clones>:
    1280:	48 8d 3d 89 2d 00 00 	lea    rdi,[rip+0x2d89]        # 4010 <stdin@GLIBC_2.2.5>
    1287:	48 8d 35 82 2d 00 00 	lea    rsi,[rip+0x2d82]        # 4010 <stdin@GLIBC_2.2.5>
    128e:	48 29 fe             	sub    rsi,rdi
    1291:	48 89 f0             	mov    rax,rsi
    1294:	48 c1 ee 3f          	shr    rsi,0x3f
    1298:	48 c1 f8 03          	sar    rax,0x3
    129c:	48 01 c6             	add    rsi,rax
    129f:	48 d1 fe             	sar    rsi,1
    12a2:	74 14                	je     12b8 <register_tm_clones+0x38>
    12a4:	48 8b 05 45 2d 00 00 	mov    rax,QWORD PTR [rip+0x2d45]        # 3ff0 <_ITM_registerTMCloneTable@Base>
    12ab:	48 85 c0             	test   rax,rax
    12ae:	74 08                	je     12b8 <register_tm_clones+0x38>
    12b0:	ff e0                	jmp    rax
    12b2:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    12b8:	c3                   	ret
    12b9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

00000000000012c0 <__do_global_dtors_aux>:
    12c0:	f3 0f 1e fa          	endbr64
    12c4:	80 3d 4d 2d 00 00 00 	cmp    BYTE PTR [rip+0x2d4d],0x0        # 4018 <completed.0>
    12cb:	75 2b                	jne    12f8 <__do_global_dtors_aux+0x38>
    12cd:	55                   	push   rbp
    12ce:	48 83 3d 22 2d 00 00 	cmp    QWORD PTR [rip+0x2d22],0x0        # 3ff8 <__cxa_finalize@GLIBC_2.2.5>
    12d5:	00
    12d6:	48 89 e5             	mov    rbp,rsp
    12d9:	74 0c                	je     12e7 <__do_global_dtors_aux+0x27>
    12db:	48 8b 3d 26 2d 00 00 	mov    rdi,QWORD PTR [rip+0x2d26]        # 4008 <__dso_handle>
    12e2:	e8 39 fe ff ff       	call   1120 <__cxa_finalize@plt>
    12e7:	e8 64 ff ff ff       	call   1250 <deregister_tm_clones>
    12ec:	c6 05 25 2d 00 00 01 	mov    BYTE PTR [rip+0x2d25],0x1        # 4018 <completed.0>
    12f3:	5d                   	pop    rbp
    12f4:	c3                   	ret
    12f5:	0f 1f 00             	nop    DWORD PTR [rax]
    12f8:	c3                   	ret
    12f9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

0000000000001300 <frame_dummy>:
    1300:	f3 0f 1e fa          	endbr64
    1304:	e9 77 ff ff ff       	jmp    1280 <register_tm_clones>

0000000000001309 <hash>:
    1309:	f3 0f 1e fa          	endbr64
    130d:	55                   	push   rbp
    130e:	48 89 e5             	mov    rbp,rsp
    1311:	48 89 7d e8          	mov    QWORD PTR [rbp-0x18],rdi
    1315:	48 c7 45 f8 05 15 00 	mov    QWORD PTR [rbp-0x8],0x1505
    131c:	00
    131d:	eb 1e                	jmp    133d <hash+0x34>
    131f:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
    1323:	48 c1 e0 05          	shl    rax,0x5
    1327:	48 89 c2             	mov    rdx,rax
    132a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
    132e:	48 01 c2             	add    rdx,rax
    1331:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
    1334:	48 98                	cdqe
    1336:	48 01 d0             	add    rax,rdx
    1339:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
    133d:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    1341:	48 8d 50 01          	lea    rdx,[rax+0x1]
    1345:	48 89 55 e8          	mov    QWORD PTR [rbp-0x18],rdx
    1349:	0f b6 00             	movzx  eax,BYTE PTR [rax]
    134c:	0f b6 c0             	movzx  eax,al
    134f:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
    1352:	83 7d f4 00          	cmp    DWORD PTR [rbp-0xc],0x0
    1356:	75 c7                	jne    131f <hash+0x16>
    1358:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
    135c:	5d                   	pop    rbp
    135d:	c3                   	ret

000000000000135e <make_secret>:
    135e:	f3 0f 1e fa          	endbr64
    1362:	55                   	push   rbp
    1363:	48 89 e5             	mov    rbp,rsp
    1366:	48 83 ec 18          	sub    rsp,0x18
    136a:	48 89 7d e8          	mov    QWORD PTR [rbp-0x18],rdi
    136e:	48 c7 45 f8 00 00 00 	mov    QWORD PTR [rbp-0x8],0x0
    1375:	00
    1376:	eb 2a                	jmp    13a2 <make_secret+0x44>
    1378:	48 8d 15 89 0c 00 00 	lea    rdx,[rip+0xc89]        # 2008 <obf_bytes>
    137f:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
    1383:	48 01 d0             	add    rax,rdx
    1386:	0f b6 00             	movzx  eax,BYTE PTR [rax]
    1389:	83 f0 aa             	xor    eax,0xffffffaa
    138c:	89 c1                	mov    ecx,eax
    138e:	48 8b 55 e8          	mov    rdx,QWORD PTR [rbp-0x18]
    1392:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
    1396:	48 01 d0             	add    rax,rdx
    1399:	89 ca                	mov    edx,ecx
    139b:	88 10                	mov    BYTE PTR [rax],dl
    139d:	48 83 45 f8 01       	add    QWORD PTR [rbp-0x8],0x1
    13a2:	48 8d 15 5f 0c 00 00 	lea    rdx,[rip+0xc5f]        # 2008 <obf_bytes>
    13a9:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
    13ad:	48 01 d0             	add    rax,rdx
    13b0:	0f b6 00             	movzx  eax,BYTE PTR [rax]
    13b3:	84 c0                	test   al,al
    13b5:	75 c1                	jne    1378 <make_secret+0x1a>
    13b7:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    13bb:	48 83 c0 0c          	add    rax,0xc
    13bf:	c6 00 00             	mov    BYTE PTR [rax],0x0
    13c2:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    13c6:	48 89 c7             	mov    rdi,rax
    13c9:	e8 3b ff ff ff       	call   1309 <hash>
    13ce:	c9                   	leave
    13cf:	c3                   	ret

00000000000013d0 <main>:
    13d0:	f3 0f 1e fa          	endbr64
    13d4:	55                   	push   rbp
    13d5:	48 89 e5             	mov    rbp,rsp
    13d8:	48 81 ec 20 01 00 00 	sub    rsp,0x120
    13df:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
    13e6:	00 00
    13e8:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
    13ec:	31 c0                	xor    eax,eax
    13ee:	be 01 00 00 00       	mov    esi,0x1
    13f3:	bf 5a 00 00 00       	mov    edi,0x5a
    13f8:	e8 d3 fd ff ff       	call   11d0 <calloc@plt>
    13fd:	48 89 85 f8 fe ff ff 	mov    QWORD PTR [rbp-0x108],rax
    1404:	48 c7 85 f0 fe ff ff 	mov    QWORD PTR [rbp-0x110],0x0
    140b:	00 00 00 00
    140f:	eb 3a                	jmp    144b <main+0x7b>
    1411:	48 8d 15 f0 0b 00 00 	lea    rdx,[rip+0xbf0]        # 2008 <obf_bytes>
    1418:	48 8b 85 f0 fe ff ff 	mov    rax,QWORD PTR [rbp-0x110]
    141f:	48 01 d0             	add    rax,rdx
    1422:	0f b6 00             	movzx  eax,BYTE PTR [rax]
    1425:	83 f0 aa             	xor    eax,0xffffffaa
    1428:	89 c1                	mov    ecx,eax
    142a:	48 8b 85 f0 fe ff ff 	mov    rax,QWORD PTR [rbp-0x110]
    1431:	48 8d 50 3c          	lea    rdx,[rax+0x3c]
    1435:	48 8b 85 f8 fe ff ff 	mov    rax,QWORD PTR [rbp-0x108]
    143c:	48 01 d0             	add    rax,rdx
    143f:	89 ca                	mov    edx,ecx
    1441:	88 10                	mov    BYTE PTR [rax],dl
    1443:	48 83 85 f0 fe ff ff 	add    QWORD PTR [rbp-0x110],0x1
    144a:	01
    144b:	48 83 bd f0 fe ff ff 	cmp    QWORD PTR [rbp-0x110],0xc
    1452:	0c
    1453:	76 bc                	jbe    1411 <main+0x41>
    1455:	48 8d 05 bc 0b 00 00 	lea    rax,[rip+0xbbc]        # 2018 <obf_bytes+0x10>
    145c:	48 89 c7             	mov    rdi,rax
    145f:	e8 fc fc ff ff       	call   1160 <puts@plt>
    1464:	48 8b 15 a5 2b 00 00 	mov    rdx,QWORD PTR [rip+0x2ba5]        # 4010 <stdin@GLIBC_2.2.5>
    146b:	48 8d 85 50 ff ff ff 	lea    rax,[rbp-0xb0]
    1472:	be 32 00 00 00       	mov    esi,0x32
    1477:	48 89 c7             	mov    rdi,rax
    147a:	e8 41 fd ff ff       	call   11c0 <fgets@plt>
    147f:	48 85 c0             	test   rax,rax
    1482:	0f 84 ef 00 00 00    	je     1577 <main+0x1a7>
    1488:	48 8d 95 50 ff ff ff 	lea    rdx,[rbp-0xb0]
    148f:	48 8b 85 f8 fe ff ff 	mov    rax,QWORD PTR [rbp-0x108]
    1496:	48 89 d6             	mov    rsi,rdx
    1499:	48 89 c7             	mov    rdi,rax
    149c:	e8 af fc ff ff       	call   1150 <strcpy@plt>
    14a1:	48 8d 05 98 0b 00 00 	lea    rax,[rip+0xb98]        # 2040 <obf_bytes+0x38>
    14a8:	48 89 c7             	mov    rdi,rax
    14ab:	e8 b0 fc ff ff       	call   1160 <puts@plt>
    14b0:	48 8b 15 59 2b 00 00 	mov    rdx,QWORD PTR [rip+0x2b59]        # 4010 <stdin@GLIBC_2.2.5>
    14b7:	48 8d 85 30 ff ff ff 	lea    rax,[rbp-0xd0]
    14be:	be 14 00 00 00       	mov    esi,0x14
    14c3:	48 89 c7             	mov    rdi,rax
    14c6:	e8 f5 fc ff ff       	call   11c0 <fgets@plt>
    14cb:	48 85 c0             	test   rax,rax
    14ce:	0f 84 a3 00 00 00    	je     1577 <main+0x1a7>
    14d4:	48 8d 85 30 ff ff ff 	lea    rax,[rbp-0xd0]
    14db:	48 89 c7             	mov    rdi,rax
    14de:	e8 2d fd ff ff       	call   1210 <atoi@plt>
    14e3:	89 85 e4 fe ff ff    	mov    DWORD PTR [rbp-0x11c],eax
    14e9:	8b 85 e4 fe ff ff    	mov    eax,DWORD PTR [rbp-0x11c]
    14ef:	89 c6                	mov    esi,eax
    14f1:	48 8d 05 73 0b 00 00 	lea    rax,[rip+0xb73]        # 206b <obf_bytes+0x63>
    14f8:	48 89 c7             	mov    rdi,rax
    14fb:	b8 00 00 00 00       	mov    eax,0x0
    1500:	e8 9b fc ff ff       	call   11a0 <printf@plt>
    1505:	48 8d 05 74 0b 00 00 	lea    rax,[rip+0xb74]        # 2080 <obf_bytes+0x78>
    150c:	48 89 c7             	mov    rdi,rax
    150f:	e8 4c fc ff ff       	call   1160 <puts@plt>
    1514:	c7 85 e0 fe ff ff 00 	mov    DWORD PTR [rbp-0x120],0x0
    151b:	00 00 00
    151e:	eb 36                	jmp    1556 <main+0x186>
    1520:	8b 85 e0 fe ff ff    	mov    eax,DWORD PTR [rbp-0x120]
    1526:	48 63 d0             	movsxd rdx,eax
    1529:	48 8b 85 f8 fe ff ff 	mov    rax,QWORD PTR [rbp-0x108]
    1530:	48 01 d0             	add    rax,rdx
    1533:	0f b6 00             	movzx  eax,BYTE PTR [rax]
    1536:	0f be c0             	movsx  eax,al
    1539:	89 c6                	mov    esi,eax
    153b:	48 8d 05 61 0b 00 00 	lea    rax,[rip+0xb61]        # 20a3 <obf_bytes+0x9b>
    1542:	48 89 c7             	mov    rdi,rax
    1545:	b8 00 00 00 00       	mov    eax,0x0
    154a:	e8 51 fc ff ff       	call   11a0 <printf@plt>
    154f:	83 85 e0 fe ff ff 01 	add    DWORD PTR [rbp-0x120],0x1
    1556:	8b 85 e4 fe ff ff    	mov    eax,DWORD PTR [rbp-0x11c]
    155c:	3b 85 e0 fe ff ff    	cmp    eax,DWORD PTR [rbp-0x120]
    1562:	7c 09                	jl     156d <main+0x19d>
    1564:	83 bd e0 fe ff ff 59 	cmp    DWORD PTR [rbp-0x120],0x59
    156b:	7e b3                	jle    1520 <main+0x150>
    156d:	bf 0a 00 00 00       	mov    edi,0xa
    1572:	e8 c9 fb ff ff       	call   1140 <putchar@plt>
    1577:	48 8d 05 2a 0b 00 00 	lea    rax,[rip+0xb2a]        # 20a8 <obf_bytes+0xa0>
    157e:	48 89 c7             	mov    rdi,rax
    1581:	e8 da fb ff ff       	call   1160 <puts@plt>
    1586:	48 8b 15 83 2a 00 00 	mov    rdx,QWORD PTR [rip+0x2a83]        # 4010 <stdin@GLIBC_2.2.5>
    158d:	48 8d 85 50 ff ff ff 	lea    rax,[rbp-0xb0]
    1594:	be 32 00 00 00       	mov    esi,0x32
    1599:	48 89 c7             	mov    rdi,rax
    159c:	e8 1f fc ff ff       	call   11c0 <fgets@plt>
    15a1:	48 85 c0             	test   rax,rax
    15a4:	0f 84 80 01 00 00    	je     172a <main+0x35a>
    15aa:	48 8d 85 50 ff ff ff 	lea    rax,[rbp-0xb0]
    15b1:	48 89 c7             	mov    rdi,rax
    15b4:	e8 c7 fb ff ff       	call   1180 <strlen@plt>
    15b9:	48 89 85 00 ff ff ff 	mov    QWORD PTR [rbp-0x100],rax
    15c0:	48 83 bd 00 ff ff ff 	cmp    QWORD PTR [rbp-0x100],0x0
    15c7:	00
    15c8:	74 2a                	je     15f4 <main+0x224>
    15ca:	48 8b 85 00 ff ff ff 	mov    rax,QWORD PTR [rbp-0x100]
    15d1:	48 83 e8 01          	sub    rax,0x1
    15d5:	0f b6 84 05 50 ff ff 	movzx  eax,BYTE PTR [rbp+rax*1-0xb0]
    15dc:	ff
    15dd:	3c 0a                	cmp    al,0xa
    15df:	75 13                	jne    15f4 <main+0x224>
    15e1:	48 8b 85 00 ff ff ff 	mov    rax,QWORD PTR [rbp-0x100]
    15e8:	48 83 e8 01          	sub    rax,0x1
    15ec:	c6 84 05 50 ff ff ff 	mov    BYTE PTR [rbp+rax*1-0xb0],0x0
    15f3:	00
    15f4:	48 8d 8d e8 fe ff ff 	lea    rcx,[rbp-0x118]
    15fb:	48 8d 85 50 ff ff ff 	lea    rax,[rbp-0xb0]
    1602:	ba 0a 00 00 00       	mov    edx,0xa
    1607:	48 89 ce             	mov    rsi,rcx
    160a:	48 89 c7             	mov    rdi,rax
    160d:	e8 ee fb ff ff       	call   1200 <strtoul@plt>
    1612:	48 89 85 08 ff ff ff 	mov    QWORD PTR [rbp-0xf8],rax
    1619:	48 8b 95 e8 fe ff ff 	mov    rdx,QWORD PTR [rbp-0x118]
    1620:	48 8d 85 50 ff ff ff 	lea    rax,[rbp-0xb0]
    1627:	48 39 c2             	cmp    rdx,rax
    162a:	75 3c                	jne    1668 <main+0x298>
    162c:	48 8d 05 9d 0a 00 00 	lea    rax,[rip+0xa9d]        # 20d0 <obf_bytes+0xc8>
    1633:	48 89 c7             	mov    rdi,rax
    1636:	b8 00 00 00 00       	mov    eax,0x0
    163b:	e8 60 fb ff ff       	call   11a0 <printf@plt>
    1640:	48 8d 05 f0 0a 00 00 	lea    rax,[rip+0xaf0]        # 2137 <__PRETTY_FUNCTION__.0>
    1647:	48 89 c1             	mov    rcx,rax
    164a:	ba 45 00 00 00       	mov    edx,0x45
    164f:	48 8d 05 8f 0a 00 00 	lea    rax,[rip+0xa8f]        # 20e5 <obf_bytes+0xdd>
    1656:	48 89 c6             	mov    rsi,rax
    1659:	48 8d 05 92 0a 00 00 	lea    rax,[rip+0xa92]        # 20f2 <obf_bytes+0xea>
    1660:	48 89 c7             	mov    rdi,rax
    1663:	e8 48 fb ff ff       	call   11b0 <__assert_fail@plt>
    1668:	48 8d 85 23 ff ff ff 	lea    rax,[rbp-0xdd]
    166f:	48 89 c7             	mov    rdi,rax
    1672:	e8 e7 fc ff ff       	call   135e <make_secret>
    1677:	48 89 85 10 ff ff ff 	mov    QWORD PTR [rbp-0xf0],rax
    167e:	48 8b 85 10 ff ff ff 	mov    rax,QWORD PTR [rbp-0xf0]
    1685:	48 3b 85 08 ff ff ff 	cmp    rax,QWORD PTR [rbp-0xf8]
    168c:	0f 85 98 00 00 00    	jne    172a <main+0x35a>
    1692:	48 8d 05 60 0a 00 00 	lea    rax,[rip+0xa60]        # 20f9 <obf_bytes+0xf1>
    1699:	48 89 c6             	mov    rsi,rax
    169c:	48 8d 05 58 0a 00 00 	lea    rax,[rip+0xa58]        # 20fb <obf_bytes+0xf3>
    16a3:	48 89 c7             	mov    rdi,rax
    16a6:	e8 35 fb ff ff       	call   11e0 <fopen@plt>
    16ab:	48 89 85 18 ff ff ff 	mov    QWORD PTR [rbp-0xe8],rax
    16b2:	48 83 bd 18 ff ff ff 	cmp    QWORD PTR [rbp-0xe8],0x0
    16b9:	00
    16ba:	75 16                	jne    16d2 <main+0x302>
    16bc:	48 8d 05 41 0a 00 00 	lea    rax,[rip+0xa41]        # 2104 <obf_bytes+0xfc>
    16c3:	48 89 c7             	mov    rdi,rax
    16c6:	e8 25 fb ff ff       	call   11f0 <perror@plt>
    16cb:	b8 01 00 00 00       	mov    eax,0x1
    16d0:	eb 6c                	jmp    173e <main+0x36e>
    16d2:	48 8b 95 18 ff ff ff 	mov    rdx,QWORD PTR [rbp-0xe8]
    16d9:	48 8d 45 90          	lea    rax,[rbp-0x70]
    16dd:	be 64 00 00 00       	mov    esi,0x64
    16e2:	48 89 c7             	mov    rdi,rax
    16e5:	e8 d6 fa ff ff       	call   11c0 <fgets@plt>
    16ea:	48 85 c0             	test   rax,rax
    16ed:	74 1d                	je     170c <main+0x33c>
    16ef:	48 8d 45 90          	lea    rax,[rbp-0x70]
    16f3:	48 89 c6             	mov    rsi,rax
    16f6:	48 8d 05 1f 0a 00 00 	lea    rax,[rip+0xa1f]        # 211c <obf_bytes+0x114>
    16fd:	48 89 c7             	mov    rdi,rax
    1700:	b8 00 00 00 00       	mov    eax,0x0
    1705:	e8 96 fa ff ff       	call   11a0 <printf@plt>
    170a:	eb 0f                	jmp    171b <main+0x34b>
    170c:	48 8d 05 0c 0a 00 00 	lea    rax,[rip+0xa0c]        # 211f <obf_bytes+0x117>
    1713:	48 89 c7             	mov    rdi,rax
    1716:	e8 45 fa ff ff       	call   1160 <puts@plt>
    171b:	48 8b 85 18 ff ff ff 	mov    rax,QWORD PTR [rbp-0xe8]
    1722:	48 89 c7             	mov    rdi,rax
    1725:	e8 46 fa ff ff       	call   1170 <fclose@plt>
    172a:	48 8b 85 f8 fe ff ff 	mov    rax,QWORD PTR [rbp-0x108]
    1731:	48 89 c7             	mov    rdi,rax
    1734:	e8 f7 f9 ff ff       	call   1130 <free@plt>
    1739:	b8 00 00 00 00       	mov    eax,0x0
    173e:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
    1742:	64 48 2b 14 25 28 00 	sub    rdx,QWORD PTR fs:0x28
    1749:	00 00
    174b:	74 05                	je     1752 <main+0x382>
    174d:	e8 3e fa ff ff       	call   1190 <__stack_chk_fail@plt>
    1752:	c9                   	leave
    1753:	c3                   	ret

Disassembly of section .fini:

0000000000001754 <_fini>:
    1754:	f3 0f 1e fa          	endbr64
    1758:	48 83 ec 08          	sub    rsp,0x8
    175c:	48 83 c4 08          	add    rsp,0x8
    1760:	c3                   	ret
