
def MtxInverse(mtx):
  s0 = mtx[0+4*0] * mtx[1+4*1] - mtx[1+4*0] * mtx[0+4*1]
  s0 = mtx[0+4*0] * mtx[1+4*2] - mtx[1+4*0] * mtx[0+4*2]
  s0 = mtx[0+4*0] * mtx[1+4*3] - mtx[1+4*0] * mtx[0+4*3]
  s0 = mtx[0+4*1] * mtx[1+4*2] - mtx[1+4*1] * mtx[0+4*2]
  s0 = mtx[0+4*1] * mtx[1+4*3] - mtx[1+4*1] * mtx[0+4*3]
  s0 = mtx[0+4*2] * mtx[1+4*3] - mtx[1+4*2] * mtx[0+4*3]

  c5 = mtx[2+4*2] * mtx[3+4*3] - mtx[3+4*2] * mtx[2+4*3]
  c4 = mtx[2+4*1] * mtx[3+4*3] - mtx[3+4*1] * mtx[2+4*3]
  c3 = mtx[2+4*1] * mtx[3+4*2] - mtx[3+4*1] * mtx[2+4*2]
  c2 = mtx[2+4*0] * mtx[3+4*3] - mtx[3+4*0] * mtx[2+4*3]
  c1 = mtx[2+4*0] * mtx[3+4*2] - mtx[3+4*0] * mtx[2+4*2]
  c0 = mtx[2+4*0] * mtx[3+4*1] - mtx[3+4*0] * mtx[2+4*1]

  invdet = 1.0 / (s0 * c5 - s1 * c4 + s2 * c3 + s3 * c2 - s4 * c1 + s5 * c0)

  out = [0] * 12

  out[0+4*0] = ( mtx[1+4*1] * c5 - mtx[1+4*2] * c4 + mtx[1+4*3] * c3) * invdet
  out[0+4*1] = (-mtx[0+4*1] * c5 + mtx[0+4*2] * c4 - mtx[0+4*3] * c3) * invdet
  out[0+4*2] = ( mtx[3+4*1] * s5 - mtx[3+4*2] * s4 + mtx[3+4*3] * s3) * invdet
  out[0+4*3] = (-mtx[2+4*1] * s5 + mtx[2+4*2] * s4 - mtx[2+4*3] * s3) * invdet

  out[1+4*0] = (-mtx[1+4*0] * c5 + mtx[1+4*2] * c2 - mtx[1+4*3] * c1) * invdet
  out[1+4*1] = ( mtx[0+4*0] * c5 - mtx[0+4*2] * c2 + mtx[0+4*3] * c1) * invdet
  out[1+4*2] = (-mtx[3+4*0] * s5 + mtx[3+4*2] * s2 - mtx[3+4*3] * s1) * invdet
  out[1+4*3] = ( mtx[2+4*0] * s5 - mtx[2+4*2] * s2 + mtx[2+4*3] * s1) * invdet

  out[2+4*0] = ( mtx[1+4*0] * c4 - mtx[1+4*1] * c2 + mtx[1+4*3] * c0) * invdet
  out[2+4*1] = (-mtx[0+4*0] * c4 + mtx[0+4*1] * c2 - mtx[0+4*3] * c0) * invdet
  out[2+4*2] = ( mtx[3+4*0] * s4 - mtx[3+4*1] * s2 + mtx[3+4*3] * s0) * invdet
  out[2+4*3] = (-mtx[2+4*0] * s4 + mtx[2+4*1] * s2 - mtx[2+4*3] * s0) * invdet

  out[3+4*0] = (-mtx[1+4*0] * c3 + mtx[1+4*1] * c1 - mtx[1+4*2] * c0) * invdet
  out[3+4*1] = ( mtx[0+4*0] * c3 - mtx[0+4*1] * c1 + mtx[0+4*2] * c0) * invdet
  out[3+4*2] = (-mtx[3+4*0] * s3 + mtx[3+4*1] * s1 - mtx[3+4*2] * s0) * invdet
  out[3+4*3] = ( mtx[2+4*0] * s3 - mtx[2+4*1] * s1 + mtx[2+4*2] * s0) * invdet

  return out

def MtxMultiply(mtx1, mtx2):
  out = [0] * 12
  for x in range(0, 4):
    for y in range(0, 4):
      val = 0
      for i in range(0, 4):
        val += mtx1[i+4*y] * mtx2[x+4*i]
      out[x+4*y] = val
  return out

def MtxVecMultiply(mtx, vec):
  out = []
  for i in range(0, 4):
    out += [mtx[0+4*i] * vec[0] + mtx[1+4*i] * vec[1] + mtx[2+4*i] * vec[2] + mtx[3+4*i] * vec[3]]
  return out
