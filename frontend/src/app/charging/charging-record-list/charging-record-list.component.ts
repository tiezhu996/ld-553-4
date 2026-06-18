import { Component, OnInit } from '@angular/core';
import { ChargingPile } from '../../shared/models/charging-pile.model';
import { ChargingRecord } from '../../shared/models/charging-record.model';
import { ApiService } from '../../shared/services/api.service';

@Component({ standalone: false,
  selector: 'app-charging-record-list',
  template: `<section class="page">
  <h1>充电记录</h1>
  <div class="toolbar">
    <mat-form-field>
      <mat-label>充电桩</mat-label>
      <mat-select [(ngModel)]="pileId" (selectionChange)="load()">
        <mat-option value="">全部桩位</mat-option>
        <mat-option *ngFor="let p of piles" [value]="p.id">{{ p.code }} - {{ p.location }}</mat-option>
      </mat-select>
    </mat-form-field>
    <mat-form-field>
      <mat-label>车牌号</mat-label>
      <input matInput [(ngModel)]="plateNumber" (keyup.enter)="load()" placeholder="输入车牌搜索" />
    </mat-form-field>
    <button mat-raised-button color="primary" (click)="load()">查询</button>
  </div>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>记录编号</th>
          <th>充电桩</th>
          <th>车牌号</th>
          <th>充电量</th>
          <th>时长</th>
          <th>费用</th>
          <th>开始时间</th>
          <th>结束时间</th>
        </tr>
      </thead>
      <tbody>
        <tr *ngFor="let r of records">
          <td>{{ r.record_no }}</td>
          <td>{{ r.pile_detail?.code || '-' }}</td>
          <td>{{ r.plate_number || '-' }}</td>
          <td>{{ r.kwh }} kWh</td>
          <td>{{ r.duration_minutes }} 分钟</td>
          <td>¥{{ r.total_fee }}</td>
          <td>{{ r.start_time | date:'yyyy-MM-dd HH:mm' }}</td>
          <td>{{ r.end_time | date:'yyyy-MM-dd HH:mm' }}</td>
        </tr>
        <tr *ngIf="records.length === 0">
          <td colspan="8" class="empty">暂无充电记录</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>`,
  styles: [`.empty{text-align:center;color:#888;padding:40px 0}`]
})
export class ChargingRecordListComponent implements OnInit {
  records: ChargingRecord[] = [];
  piles: ChargingPile[] = [];
  pileId = '';
  plateNumber = '';

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.loadPiles();
    this.load();
  }

  loadPiles(): void {
    this.api.listPiles().subscribe(piles => this.piles = piles);
  }

  load(): void {
    const filters: Record<string, string> = {};
    if (this.pileId) filters['pile_id'] = String(this.pileId);
    if (this.plateNumber) filters['plate_number'] = this.plateNumber;
    this.api.listChargingRecords(filters).subscribe(records => this.records = records);
  }
}
